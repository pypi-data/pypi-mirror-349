import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import itertools
import datetime
import time
import sys
from sklearn.model_selection import train_test_split
from collections import defaultdict

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torch.optim.lr_scheduler import LambdaLR

import numpy as np
import random
from lightning.pytorch import seed_everything


from ._model_framework import *

torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = True

class UNST(nn.Module):
    def __init__(self, adata = None, task_name=None, conditionA=None, conditionB=None,
                 n_epochs=300, decay_start_epoch = 100, patience = 50, freeze_gan_epoch = 75, save_epoch=150,
                 n_hidden=256, n_latent=128,
                 n_layers=3, n_shared_block=1, n_layers_D=2,
                 all_lambda=[0.1, 0.001, 100, 0.001, 100, 100, 1], 
                 lr_D=0.0001, lr_G=0.0001,
                 beta=[0.5,0.999], 
                 batch_size=32,
                 val_rate=0.1,
                 Dropout=0.1
                ):
        super(UNST, self).__init__()
        """
        UscKO: Unsupervised Single Cell RNA-seq virtual perturbation KnockOut tools. UscKO is an unsupervised virtual perturbation and knockout tool for scRNA-seq, which can be used for style transfer and simulating gene KO experiments on scRNA-seq data.
        
        Unsupervised scRNA-seq Style Transfer Trainer(UNST)
        
        Arguments:
        - adata (AnnData, required): An AnnData object generated form 'Preparation'. 
        - task_name (str, required): Used for naming and saving the model weights.
        - conditionA (str, required): The original condition in the snRNA-seq data. Must match a value in `adata.obs['Condition']`.
        - conditionB (str, required): The target condition of snRNA-seq. Must match a value in `adata.obs['Condition']`.
        - n_epochs (int, required): Total number of training epochs. Default is 300.
        - decay_start_epoch (int, required): The epoch at which learning rate decay begins. Default is 100.
        - patience (int, required): Number of epochs with no improvement after which early stopping is triggered. Default is 25.
        - freeze_gan_epoch (int, required): Number of epochs for the initial stage of training during which the GAN components are frozen. Default is 75.
        - save_epoch (int, required): Epoch from which model checkpoints begin to be saved. Default is 150.
        - n_hidden (int, required): Number of nodes per hidden layer in the neural networks. Default is 256.
        - n_latent (int, required): Dimensionality of the latent space. Default is 50.
        - n_layers (int, required): Number of hidden layers used for the encoder and decoder. Default is 3.
        - n_shared_block (int, required): Number of shared layers used for encoder and decoder. Default is 1.
        - n_layers_D (int, required): Number of hidden layers in the discriminator. Default is 2.
        - all_lambda (list, required): List of loss function weights for different components of the model. Default is [0.1, 0.001, 100, 0.001, 100, 100, 1].
        - lr_D (float, required): Learning rate for the discriminator. Default is 0.0001.
        - lr_G (float, required): Learning rate for the encoder and decoder. Default is 0.0001.
        - beta (list, required): Decay rates of first and second order momentum of gradients for the Adam optimizer. Default is [0.5, 0.999].
        - batch_size (int, required): Batch size for training. Default is 32.
        - val_rate (float, optional):Proportion of cells used as the validation set. Must be a float between 0 and 1. Default is 0.1.
        - Dropout (float, optional): Dropout rate for neural networks, ranging from 0 to 1. Default is 0.1.
        """

        #########################
        # Device detected
        #########################
        if torch.cuda.is_available():
            print("CUDA device detected. Using GPU for computation.")
        else:
            print("[Warning] No CUDA-enabled GPU detected. Falling back to CPU for computation.")
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        #################################
        # Create checkpoint directories
        #################################
        self.task_name = task_name
        if self.task_name is None:
            raise ValueError("Task name must be provided")

        self.save_models_dir = "./saved_models/%s/" % self.task_name
        os.makedirs(self.save_models_dir, exist_ok=True)
        
        self.save_models_dir = self.save_models_dir
        
        #########################
        # LOSSES
        #########################
        self.criterion_GAN = torch.nn.MSELoss()
        self.criterion_VAE = torch.nn.MSELoss(reduction='sum') # SSE

        def kl_divergence(q_dist):
            q_mean, q_std = q_dist.loc, q_dist.scale
            q_var = q_std.pow(2)  # σ² = (exp(z_log_var/2))^2 = exp(z_log_var)
            # p_var = 1.0 p_mean = 0
            
            kl = 0.5 * (q_var + q_mean.pow(2) - 1 - torch.log(q_var))
            return kl
        
        self.KL = kl_divergence
        
        # base settings
        self.adata = adata.adata_Train
        self.data_size = self.adata.X.shape[1]
        self.n_epochs = n_epochs
        self.decay_start_epoch = decay_start_epoch
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.n_latent = n_latent
        self.n_layers_D = n_layers_D
        self.conditionA = conditionA
        self.conditionB = conditionB
        self.batch_size = batch_size
        self.val_rate = val_rate
        self.Test_loss = float('inf')
        self.n_shared_block= n_shared_block
        self.Dropout = Dropout
        
        self.Cell_name = adata.Cell_name
        
        self.freeze_gan_epoch = freeze_gan_epoch
        self.save_epoch = save_epoch
        
        self.patience = patience
        self.delta = 1
        self.patience_counter = 0
        
        if self.conditionA not in self.adata.obs['Condition'].values or self.conditionB not in self.adata.obs['Condition'].values:
            raise ValueError(f"'conditionA or conditionB is not in the {self.adata.obs['Condition']}.")

        seed = 666
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        
        
        # Initialize generator and discriminator
        self.shared_E = SharedLayers_E(features=self.n_hidden, n_latent=self.n_latent, Dropout=self.Dropout, n_shared_block=self.n_shared_block)
        self.shared_G = SharedLayers_G(features=self.n_hidden, n_latent=self.n_latent, Dropout=self.Dropout, n_shared_block=self.n_shared_block)
        
        self.E1 = Encoder(data_size=self.data_size, n_hidden=self.n_hidden, n_latent=self.n_latent, n_layers=self.n_layers, shared_block=self.shared_E, Dropout=self.Dropout)
        self.E2 = Encoder(data_size=self.data_size, n_hidden=self.n_hidden, n_latent=self.n_latent, n_layers=self.n_layers, shared_block=self.shared_E, Dropout=self.Dropout)

        self.G1 = Generator(n_latent=self.n_latent, n_hidden=self.n_hidden, data_size=self.data_size, shared_block=self.shared_G, n_layers=self.n_layers, Dropout=self.Dropout)
        self.G2 = Generator(n_latent=self.n_latent, n_hidden=self.n_hidden, data_size=self.data_size, shared_block=self.shared_G,n_layers=self.n_layers, Dropout=self.Dropout)
        
        self.D1 = Discriminator(data_size=self.data_size, n_hidden=self.n_hidden, n_layers_D=self.n_layers_D, Dropout=self.Dropout)
        self.D2 = Discriminator(data_size=self.data_size, n_hidden=self.n_hidden, n_layers_D=self.n_layers_D, Dropout=self.Dropout)
        
        # init weights
        for module in [self.shared_E, self.shared_G, self.E1, self.E2, self.G1, self.G2, self.D1, self.D2]:
            module.apply(init_weights)
        print("All modules init weights completed")
        
        # device to cuda or cpu
        self.E1.to(self.device)
        self.E2.to(self.device)
        self.G1.to(self.device)
        self.G2.to(self.device)
        self.D1.to(self.device)
        self.D2.to(self.device)
        self.criterion_GAN.to(self.device)
        self.criterion_VAE.to(self.device)
        
        # Loss weights lambda
        self.all_lambda = all_lambda
        scale = 39624 / self.data_size

        self.lambda_0 = self.all_lambda[0] # GAN
        self.lambda_1 = self.all_lambda[1] # KL (encoded scrna-seq)
        self.lambda_2 = self.all_lambda[2] * scale # recon
        self.lambda_3 = self.all_lambda[3] # KL (encoded translated scrna-seq)
        self.lambda_4 = self.all_lambda[4] * scale # Cycle
        self.lambda_5 = self.all_lambda[5] * scale # translate
        self.lambda_6 = self.all_lambda[6] # ZINB NNL
        
        # Optimizers
        self.lr_D = lr_D
        self.lr_G = lr_G
        self.b1 = beta[0]
        self.b2 = beta[1]
        
        params = itertools.chain(self.E1.parameters(), self.E2.parameters(), self.G1.parameters(), self.G2.parameters())
        unique_params = list(dict.fromkeys(params))
        self.optimizer_G = torch.optim.Adam(unique_params, lr=self.lr_G, betas=(self.b1, self.b2))
        
        self.optimizer_D1 = torch.optim.Adam(self.D1.parameters(), lr=self.lr_D, betas=(self.b1, self.b2))
        self.optimizer_D2 = torch.optim.Adam(self.D2.parameters(), lr=self.lr_D, betas=(self.b1, self.b2))
        
        # Learning rate update schedulers
        self.lr_scheduler_G = LambdaLR(self.optimizer_G, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step) 
        self.lr_scheduler_D1 = LambdaLR(self.optimizer_D1, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step)
        self.lr_scheduler_D2 = LambdaLR(self.optimizer_D2, lr_lambda=LambdaLR2(self.n_epochs, self.decay_start_epoch).step)
        
        # scRNA-seq data processing
        self.scRNA_1 = self.adata[(self.adata.obs["Condition"] == self.conditionA)]
        self.scRNA_2 = self.adata[(self.adata.obs["Condition"] == self.conditionB)]

        cell_types_1 = self.scRNA_1.obs[self.Cell_name].values
        cell_types_2 = self.scRNA_2.obs[self.Cell_name].values
        
        self.scRNA_1, self.scRNA_1_test= train_test_split(self.scRNA_1, test_size=self.val_rate, stratify=cell_types_1)
        self.scRNA_2, self.scRNA_2_test= train_test_split(self.scRNA_2, test_size=self.val_rate, stratify=cell_types_2)
        
        self.scRNA_1.X = self.scRNA_1.X.toarray()
        self.scRNA_2.X = self.scRNA_2.X.toarray()
        self.scRNA_1_test.X = self.scRNA_1_test.X.toarray()
        self.scRNA_2_test.X = self.scRNA_2_test.X.toarray()
        del self.adata
        
        # Create Data_Loader
        self.data_loader = self.create_data_loader()
        self.test_data_loader = self.create_test_data_loader()

    #########################
    # Save model weight 
    #########################
    def save_model_weight(self, save_models_dir, epoch):
        
        save_path = os.path.join(self.save_models_dir, f"{self.task_name}_Best_Weights.pth")
        
        epochs = epoch
        torch.save({
            'E1_state_dict': self.E1.state_dict(),
            'E2_state_dict': self.E2.state_dict(),
            'G1_state_dict': self.G1.state_dict(),
            'G2_state_dict': self.G2.state_dict()
        }, save_path)
        print(f"Model saved at {save_models_dir} for epoch {epochs}\n")
    
    #########################
    # Data Loader for Training
    #########################
    def create_data_loader(self):
        class PairedCellDataset(Dataset):
            def __init__(self, scRNA_1, scRNA_2, batch_size):
                self.batch_size = batch_size
                
                self.scRNA_1_X = scRNA_1.X.toarray()
                self.scRNA_2_X = scRNA_2.X.toarray()
                
                self.type_indices_1 = self._group_indices(scRNA_1)
                self.type_indices_2 = self._group_indices(scRNA_2)
                
                self.common_types = sorted(set(self.type_indices_1.keys()) & set(self.type_indices_2.keys()))
                assert len(self.common_types) > 0, "No common cell types found!"
                
                self.paired_indices = self._generate_aligned_pairs()
            
            def _group_indices(self, adata):
                type_dict = defaultdict(list)
                for idx, cell_type in enumerate(adata.obs["Cell_type"]):
                    type_dict[cell_type].append(idx)
                return type_dict
            
            def _generate_aligned_pairs(self):
                all_pairs = []
                
                for cell_type in self.common_types:
                    indices_1 = self.type_indices_1[cell_type]
                    indices_2 = self.type_indices_2[cell_type]
                    
                    num_pairs = max(len(indices_1), len(indices_2))
                    padded_num = ((num_pairs + self.batch_size - 1) // self.batch_size) * self.batch_size
                    
                    indices_1_sampled = np.random.choice(indices_1, size=padded_num, replace=True)
                    indices_2_sampled = np.random.choice(indices_2, size=padded_num, replace=True)

                    pairs = list(zip(indices_1_sampled, indices_2_sampled))
                    all_pairs.extend(pairs)

                return all_pairs
            
            def __len__(self):
                return len(self.paired_indices)
            
            def __getitem__(self, idx):
                i, j = self.paired_indices[idx]
                return (self.scRNA_1_X[i].astype(np.float32), self.scRNA_2_X[j].astype(np.float32))

        dataset = PairedCellDataset(self.scRNA_1, self.scRNA_2, self.batch_size)
        
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=True, drop_last=False)
        del self.scRNA_1, self.scRNA_2
        return loader

    #########################
    # Data Loader for Testing
    #########################
    def create_test_data_loader(self):
        class PairedCellDataset(Dataset):
            def __init__(self, scRNA_1_test, scRNA_2_test, batch_size):
                self.batch_size = batch_size
                
                self.scRNA_1_X = scRNA_1_test.X.toarray()
                self.scRNA_2_X = scRNA_2_test.X.toarray()
                
                self.type_indices_1 = self._group_indices(scRNA_1_test)
                self.type_indices_2 = self._group_indices(scRNA_2_test)
                
                self.common_types = sorted(set(self.type_indices_1.keys()) & set(self.type_indices_2.keys()))
                assert len(self.common_types) > 0, "No common cell types found!"
                
                self.paired_indices = self._generate_aligned_pairs()
            
            def _group_indices(self, adata):
                type_dict = defaultdict(list)
                for idx, cell_type in enumerate(adata.obs["Cell_type"]):
                    type_dict[cell_type].append(idx)
                return type_dict
            
            def _generate_aligned_pairs(self):
                all_pairs = []
                
                for cell_type in self.common_types:
                    indices_1 = self.type_indices_1[cell_type]
                    indices_2 = self.type_indices_2[cell_type]
                    
                    num_pairs = max(len(indices_1), len(indices_2))
                    padded_num = ((num_pairs + self.batch_size - 1) // self.batch_size) * self.batch_size
                    
                    indices_1_sampled = np.random.choice(indices_1, size=padded_num, replace=True)
                    indices_2_sampled = np.random.choice(indices_2, size=padded_num, replace=True)

                    pairs = list(zip(indices_1_sampled, indices_2_sampled))
                    all_pairs.extend(pairs)

                return all_pairs
            
            def __len__(self):
                return len(self.paired_indices)
            
            def __getitem__(self, idx):
                i, j = self.paired_indices[idx]
                return (self.scRNA_1_X[i].astype(np.float32), self.scRNA_2_X[j].astype(np.float32))

        dataset = PairedCellDataset(self.scRNA_1_test, self.scRNA_2_test, self.batch_size)
        
        loader = DataLoader(dataset, batch_size=self.batch_size, shuffle=False, drop_last=False)
        del self.scRNA_1_test, self.scRNA_2_test
        return loader

    #########################
    # Test evaluation
    #########################
    def Test(self):
        self.E1.eval()
        self.E2.eval()
        self.G1.eval()
        self.G2.eval()
        self.D1.eval()
        self.D2.eval()
        
        with torch.no_grad():
            total_loss_G = 0.0
            num_batches = 0
            mini_batch_count2 = 1
            
            for i,batch in enumerate(self.test_data_loader):
                self.X1, self.X2 = batch

                self.X1 = self.X1.to(self.device)
                self.X2 = self.X2.to(self.device)
                
                #########################
                #  Train E and G
                #########################
                # Get shared latent representation
                self.qz1, self.Z1 = self.E1(self.X1, training=False)
                self.qz2, self.Z2 = self.E2(self.X2, training=False)

                # Reconstruct scRNA-seq
                self.recon_X1_mu, self.recon_X1_log_prob = self.G1(self.Z1, self.X1, training=True)
                self.recon_X2_mu, self.recon_X2_log_prob = self.G2(self.Z2, self.X2, training=True)
                
                # Translate scRNA-seq
                self.fake_X1_mu, self.fake_X1_log_prob = self.G1(self.Z2, self.X2, training=True)
                self.fake_X2_mu, self.fake_X2_log_prob = self.G2(self.Z1, self.X1, training=True)
                
                # Cycle translation
                self.qz1_, self.Z1_ = self.E1(self.fake_X1_mu, training=False)
                self.qz2_, self.Z2_ = self.E2(self.fake_X2_mu, training=False)
                
                self.cycle_X1_mu, self.cycle_X1_log_prob = self.G1(self.Z2_, self.fake_X2_mu, training=True)
                self.cycle_X2_mu, self.cycle_X2_log_prob = self.G2(self.Z1_, self.fake_X1_mu, training=True)

                
                self.Z1 = self.Z1.to(self.device)
                self.Z2 = self.Z2.to(self.device)
                self.recon_X1_mu = self.recon_X1_mu.to(self.device)
                self.recon_X2_mu = self.recon_X2_mu.to(self.device)
                self.fake_X1_mu = self.fake_X1_mu.to(self.device)
                self.fake_X2_mu = self.fake_X2_mu.to(self.device)
                self.Z1_ = self.Z1_.to(self.device)
                self.Z2_ = self.Z2_.to(self.device)
                self.cycle_X1_mu = self.cycle_X1_mu.to(self.device)
                self.cycle_X2_mu = self.cycle_X2_mu.to(self.device)

                self.recon_X1_log_prob = self.recon_X1_log_prob.to(self.device)
                self.recon_X2_log_prob = self.recon_X2_log_prob.to(self.device)
                self.fake_X1_log_prob = self.fake_X1_log_prob.to(self.device)
                self.fake_X2_log_prob = self.fake_X2_log_prob.to(self.device)
                self.cycle_X1_log_prob = self.cycle_X1_log_prob.to(self.device)
                self.cycle_X2_log_prob = self.cycle_X2_log_prob.to(self.device)
                

                # Losses MSEloss = loss/(batchsize * feature)
                out1 = self.D1(self.fake_X1_mu)
                out2 = self.D2(self.fake_X2_mu)
                self.loss_GAN_1 = self.lambda_0 * -out1.mean()
                self.loss_GAN_2 = self.lambda_0 * -out2.mean()
                
                # .sum(dim=1).mean(dim=0) = loss/(batchsize)  .sum(dim=1).mean(dim=0) = loss/(batchsize * feature)
                self.loss_KL_1 = self.lambda_1 * self.KL(self.qz1).sum(dim=1).mean()
                self.loss_KL_2 = self.lambda_1 * self.KL(self.qz2).sum(dim=1).mean()
                
                # recon loss
                self.loss_recon_1 = self.lambda_2 * self.criterion_VAE(self.recon_X1_mu, self.X1)
                self.loss_recon_2 = self.lambda_2 * self.criterion_VAE(self.recon_X2_mu, self.X2)
                
                # cyc KL 
                self.loss_KL_1_ = self.lambda_3 * self.KL(self.qz1_).sum(dim=1).mean()
                self.loss_KL_2_ = self.lambda_3 * self.KL(self.qz2_).sum(dim=1).mean()
                
                # cyc loss
                self.loss_cyc_1 = self.lambda_4 * self.criterion_VAE(self.cycle_X1_mu, self.X1)
                self.loss_cyc_2 = self.lambda_4 * self.criterion_VAE(self.cycle_X2_mu, self.X2)
                
                # translate loss
                self.loss_translate_1 = self.lambda_5 * self.criterion_VAE(self.fake_X1_mu, self.X1)
                self.loss_translate_2 = self.lambda_5 * self.criterion_VAE(self.fake_X2_mu, self.X2)

                # NNL for ZINB
                self.loss_recon_X1_log_prob = self.lambda_6 * -self.recon_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_recon_X2_log_prob = self.lambda_6 * -self.recon_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X1_log_prob = self.lambda_6 * -self.fake_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X2_log_prob = self.lambda_6 * -self.fake_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X1_log_prob = self.lambda_6 * -self.cycle_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X2_log_prob = self.lambda_6 * -self.cycle_X2_log_prob.sum(dim=1).mean(dim=0)

                
                self.loss_G = (
                    self.loss_GAN_1 + self.loss_GAN_2
                    + self.loss_KL_1 + self.loss_KL_2 
                    + self.loss_recon_1 + self.loss_recon_2 
                    + self.loss_KL_1_ + self.loss_KL_2_ 
                    + self.loss_cyc_1 + self.loss_cyc_2
                    + self.loss_translate_1 + self.loss_translate_2
                    + self.loss_recon_X1_log_prob + self.loss_recon_X2_log_prob
                    + self.loss_fake_X1_log_prob + self.loss_fake_X2_log_prob
                    + self.loss_cycle_X1_log_prob + self.loss_cycle_X2_log_prob
                )
                
                total_loss_G += self.loss_G.item()
                num_batches += 1*self.test_data_loader.batch_size
                
        Test_loss = total_loss_G / num_batches
        
        print("Test Loss: {:.3e}\n".format(Test_loss))
            
        self.E1.train()
        self.E2.train()
        self.G1.train()
        self.G2.train()
        self.D1.train()
        self.D2.train()
        
        return Test_loss
    
    
    #########################
    #  Training
    #########################
    def train(self):
        Test_iterator = iter(self.test_data_loader)
        best_Test_loss = float('inf')
        self.prev_time = time.time()
        
        for epoch in range(1, self.n_epochs + 1):
            Test_losses = []
            
            mini_batch_count = 1
            cum_loss_G = 0.0
            cum_loss_D1 = 0.0
            cum_loss_D2 = 0.0

            for i, batch in enumerate(self.data_loader):

                self.X1, self.X2 = batch
                
                self.X1 = self.X1.to(self.device)
                self.X2 = self.X2.to(self.device)
                
                try:
                    Test_batch = next(Test_iterator)
                except StopIteration:
                    Test_iterator = iter(self.test_data_loader)
                    Test_batch = next(Test_iterator)
                
                #########################
                #  Train E and G
                #########################
                self.optimizer_G.zero_grad()
                # Get shared latent representation
                self.qz1, self.Z1 = self.E1(self.X1, training=True)
                self.qz2, self.Z2 = self.E2(self.X2, training=True)
                
                # Reconstruct scRNA-seq
                self.recon_X1_mu, self.recon_X1_log_prob = self.G1(self.Z1, self.X1, training=True)
                self.recon_X2_mu, self.recon_X2_log_prob = self.G2(self.Z2, self.X2, training=True)
                
                # Translate scRNA-seq
                self.fake_X1_mu, self.fake_X1_log_prob = self.G1(self.Z2, self.X2, training=True)
                self.fake_X2_mu, self.fake_X2_log_prob = self.G2(self.Z1, self.X1, training=True)
                
                # Cycle translation
                self.qz1_, self.Z1_ = self.E1(self.fake_X1_mu, training=True)
                self.qz2_, self.Z2_ = self.E2(self.fake_X2_mu, training=True)
                
                self.cycle_X1_mu, self.cycle_X1_log_prob = self.G1(self.Z2_, self.fake_X2_mu, training=True)
                self.cycle_X2_mu, self.cycle_X2_log_prob = self.G2(self.Z1_, self.fake_X1_mu, training=True)

                
                self.Z1 = self.Z1.to(self.device)
                self.Z2 = self.Z2.to(self.device)
                self.recon_X1_mu = self.recon_X1_mu.to(self.device)
                self.recon_X2_mu = self.recon_X2_mu.to(self.device)
                self.fake_X1_mu = self.fake_X1_mu.to(self.device)
                self.fake_X2_mu = self.fake_X2_mu.to(self.device)
                self.Z1_ = self.Z1_.to(self.device)
                self.Z2_ = self.Z2_.to(self.device)
                self.cycle_X1_mu = self.cycle_X1_mu.to(self.device)
                self.cycle_X2_mu = self.cycle_X2_mu.to(self.device)

                self.recon_X1_log_prob = self.recon_X1_log_prob.to(self.device)
                self.recon_X2_log_prob = self.recon_X2_log_prob.to(self.device)
                self.fake_X1_log_prob = self.fake_X1_log_prob.to(self.device)
                self.fake_X2_log_prob = self.fake_X2_log_prob.to(self.device)
                self.cycle_X1_log_prob = self.cycle_X1_log_prob.to(self.device)
                self.cycle_X2_log_prob = self.cycle_X2_log_prob.to(self.device)


                
                # Losses
                out1 = self.D1(self.fake_X1_mu)
                out2 = self.D2(self.fake_X2_mu)
                self.loss_GAN_1 = self.lambda_0 * -out1.mean()
                self.loss_GAN_2 = self.lambda_0 * -out2.mean()
                
                self.loss_KL_1 = self.lambda_1 * self.KL(self.qz1).sum(dim=1).mean()
                self.loss_KL_2 = self.lambda_1 * self.KL(self.qz2).sum(dim=1).mean()

                self.loss_recon_1 = self.lambda_2 * self.criterion_VAE(self.recon_X1_mu, self.X1)
                self.loss_recon_2 = self.lambda_2 * self.criterion_VAE(self.recon_X2_mu, self.X2)

                self.loss_KL_1_ = self.lambda_3 * self.KL(self.qz1_).sum(dim=1).mean()
                self.loss_KL_2_ = self.lambda_3 * self.KL(self.qz2_).sum(dim=1).mean()
                
                self.loss_cyc_1 = self.lambda_4 * self.criterion_VAE(self.cycle_X1_mu, self.X1)
                self.loss_cyc_2 = self.lambda_4 * self.criterion_VAE(self.cycle_X2_mu, self.X2)

                self.loss_translate_1 = self.lambda_5 * self.criterion_VAE(self.fake_X1_mu, self.X1)
                self.loss_translate_2 = self.lambda_5 * self.criterion_VAE(self.fake_X2_mu, self.X2)

                self.loss_recon_X1_log_prob = self.lambda_6 * -self.recon_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_recon_X2_log_prob = self.lambda_6 * -self.recon_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X1_log_prob = self.lambda_6 * -self.fake_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_fake_X2_log_prob = self.lambda_6 * -self.fake_X2_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X1_log_prob = self.lambda_6 * -self.cycle_X1_log_prob.sum(dim=1).mean(dim=0)
                self.loss_cycle_X2_log_prob = self.lambda_6 * -self.cycle_X2_log_prob.sum(dim=1).mean(dim=0)


                if epoch < self.freeze_gan_epoch:
                    for p in self.D1.parameters():
                        p.requires_grad = False
                    for p in self.D2.parameters():
                        p.requires_grad = False
                else:
                    for p in self.D1.parameters():
                        p.requires_grad = True
                    for p in self.D2.parameters():
                        p.requires_grad = True
                
                if epoch < self.freeze_gan_epoch:
                    self.loss_G = (
                        self.loss_KL_1 + self.loss_KL_2 
                        + self.loss_recon_1 + self.loss_recon_2 
                        + self.loss_recon_X1_log_prob + self.loss_recon_X2_log_prob
                    )
                else:
                    self.loss_G = (
                        self.loss_GAN_1 + self.loss_GAN_2
                        + self.loss_KL_1 + self.loss_KL_2 
                        + self.loss_recon_1 + self.loss_recon_2 
                        + self.loss_KL_1_ + self.loss_KL_2_ 
                        + self.loss_cyc_1 + self.loss_cyc_2
                        + self.loss_translate_1 + self.loss_translate_2
                        + self.loss_recon_X1_log_prob + self.loss_recon_X2_log_prob
                        + self.loss_fake_X1_log_prob + self.loss_fake_X2_log_prob
                        + self.loss_cycle_X1_log_prob + self.loss_cycle_X2_log_prob
                    )
                self.loss_G = self.loss_G.float()
                cum_loss_G += self.loss_G.item()

                self.loss_G.backward()
                self.optimizer_G.step()
                
                torch.cuda.empty_cache()
                #########################
                #  Train Discriminator 1
                #########################
                def compute_gradient_penalty(D, real_samples, fake_samples):
                    alpha = torch.rand(real_samples.size(0), 1).to(real_samples.device)
                    interpolates = (alpha * real_samples + (1 - alpha) * fake_samples).requires_grad_(True)
                    d_interpolates = D(interpolates)
                    gradients = torch.autograd.grad(
                        outputs=d_interpolates,
                        inputs=interpolates,
                        grad_outputs=torch.ones_like(d_interpolates),
                        create_graph=True,
                        retain_graph=True,
                        only_inputs=True,
                    )[0]
                    gradients = gradients.view(gradients.size(0), -1)
                    gradient_norms = gradients.norm(2, dim=1)
                    gradient_penalty = ((gradient_norms - 1) ** 2).mean()
                    return gradient_penalty
                
                if epoch >= self.freeze_gan_epoch:
                
                    self.optimizer_D1.zero_grad()

                    d1_real = self.D1(self.X1)
                    d1_fake = self.D1(self.fake_X1_mu.detach())

                    # gradient_penalty
                    gp1 = compute_gradient_penalty(self.D1, self.X1, self.fake_X1_mu.detach())
                    gamma_gp = 10
                    self.loss_D1 = d1_fake.mean() - d1_real.mean() + gamma_gp * gp1

                    cum_loss_D1 += self.loss_D1.item()
                    self.loss_D1.backward()
                    self.optimizer_D1.step()
                
                #########################
                #  Train Discriminator 2
                #########################
                    self.optimizer_D2.zero_grad()

                    d2_real = self.D2(self.X2)
                    d2_fake = self.D2(self.fake_X2_mu.detach())
                
                    gp2 = compute_gradient_penalty(self.D2, self.X2, self.fake_X2_mu.detach())
                    gamma_gp = 10
                    self.loss_D2 = d2_fake.mean() - d2_real.mean() + gamma_gp * gp2
                
                    cum_loss_D2 += self.loss_D2.item()
                    self.loss_D2.backward()
                    self.optimizer_D2.step()
                #########################
                #  Log Progress
                #########################
                mini_batch_count += 1*self.data_loader.batch_size
                ave_loss_G = cum_loss_G / mini_batch_count
                ave_loss_D1 = cum_loss_D1 / mini_batch_count
                ave_loss_D2 = cum_loss_D2 / mini_batch_count
                
                   
                # Determine approximate time left
                current_time = time.time()
                self.batches_done = epoch * len(self.data_loader) + i
                self.batches_left = self.n_epochs * len(self.data_loader) - self.batches_done
                
                time_per_batch = current_time - self.prev_time
                self.prev_time = current_time
                
                if self.batches_left > 0:
                    self.time_left = datetime.timedelta(seconds=self.batches_left * time_per_batch)
                else:
                    self.time_left = datetime.timedelta(seconds=0)
                    
                eta_str = str(self.time_left).split('.')[0]
                
                
                
                if epoch < self.freeze_gan_epoch:
                    g_loss = (self.loss_G / self.data_loader.batch_size).item()
                    sys.stdout.write(
                        f"\r[Epoch {epoch}/{self.n_epochs}] [Batch {i}/{len(self.data_loader)}] [G loss: {g_loss:.4f}] ETA： {eta_str}   ")
                    sys.stdout.flush()
                else:
                    d_loss = ((self.loss_D1 + self.loss_D2) / self.data_loader.batch_size).item()
                    g_loss = (self.loss_G / self.data_loader.batch_size).item()
                    sys.stdout.write(
                        f"\r[Epoch {epoch}/{self.n_epochs}] [Batch {i}/{len(self.data_loader)}] [D loss: {d_loss:.4f}] [G loss: {g_loss:.4f}] ETA: {eta_str}   ")
                    sys.stdout.flush()
                    
                if (i + 1) == len(self.data_loader):
                    if epoch < self.freeze_gan_epoch:
                        print(f"\n[Epoch {epoch}/{self.n_epochs}] [Ave_G loss: {ave_loss_G:.3e}]")
                    else:
                        print(f"\n[Epoch {epoch}/{self.n_epochs}] [Ave_D1 loss: {ave_loss_D1:.3e}] [Ave_D2 loss: {ave_loss_D2:.3e}] [Ave_G loss: {ave_loss_G:.3e}]")
            
            Test_loss = self.Test()
            Test_losses.append(Test_loss)
            
            # early stop
            if epoch > self.save_epoch :
                if Test_loss < best_Test_loss - self.delta:
                    best_Test_loss = Test_loss
                    self.patience_counter = 0
                    self.save_model_weight(self.save_models_dir, epoch) 
                else:
                    self.patience_counter += 1
                
                if self.patience_counter > self.patience:
                    print(f"\nEarly stopping triggered at epoch {epoch}!")
                    break
            
            # Update learning rates
            if epoch < self.freeze_gan_epoch:
                self.lr_scheduler_G.step()
            else:
                self.lr_scheduler_G.step()
                self.lr_scheduler_D1.step()
                self.lr_scheduler_D2.step()