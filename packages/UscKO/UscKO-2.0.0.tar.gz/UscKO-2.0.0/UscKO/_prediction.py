import os

import torch
import torch.nn as nn
import anndata as ad
from torch.utils.data import Dataset, DataLoader
import numpy as np

import numpy as np
import random

from ._model_framework import *

class Prediction(nn.Module):
    def __init__(self, adata=None, task_name=None, 
                 weights_folder="./saved_models/",
                 n_hidden=256, 
                 n_latent=128, 
                 n_layers=3, 
                 n_shared_block=1,
                 batch_size=32,
                 KO_mode= True,
                ):
        super(Prediction, self).__init__()
        """
        ScRNA-seq style transfer and virtual KnockOut generator.
        
        Arguments:
        - adata (AnnData, required): An AnnData object generated from 'Preparation'.
        - task_name (str, required): Name of the training task and the saved weights.
        - weights_folder (str, optional): Path to the folder containing the weights. Default is "./saved_models/".
        - n_hidden (int, required): Number of nodes per hidden layer in the neural networks. Default is 256.
        - n_latent (int, required): Dimensionality of the latent space. Default is 50.
        - n_layers (int, required): Number of hidden layers used for the encoder neural networks. Default is 5.
        - n_shared_block (int, required): Number of shared layers used for encoder and decoder neural networks. Default is 1.
        - batch_size (int, required): Batch size for training. Default is 1.
        - K0_mode (Boolean, required): Virtual Knockout Mode. Default is True.
        """
        # Device detected
        if torch.cuda.is_available():
            print("CUDA device detected. Using GPU for computations.")
        else:
            print("Warning: No CUDA device detected. Using CPU for computations.")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        # Initialize
        self.adata = adata.adata_Perturbation
        
        if isinstance(KO_mode, bool):
            if KO_mode is True:
                self.adata_KO = adata.adata_Perturbation_KO
            else:
                pass
        else:
            raise ValueError("KO_mode should be a boolean value.")

        self.data_size = self.adata.X.shape[1]
        self.task_name = task_name
        self.batch_size = batch_size
        self.n_latent = n_latent
        self.n_hidden = n_hidden
        self.n_layers = n_layers
        self.n_shared_block = n_shared_block
        self.Dropout = 0
        self.KO_mode = KO_mode
        self.weights_folder = weights_folder

        self.model_initialized = False
        
    def _initialize_model(self, force_reload=False):
        if self.model_initialized and not force_reload:
            return
        
        seed = 666
        random.seed(seed)
        np.random.seed(seed)
        torch.manual_seed(seed)
        if torch.cuda.is_available():
            torch.cuda.manual_seed(seed)
            torch.cuda.manual_seed_all(seed)
            torch.backends.cudnn.deterministic = True
            torch.backends.cudnn.benchmark = False
        
        # Initialize generator
        self.shared_E = SharedLayers_E(features=self.n_hidden, n_latent=self.n_latent, Dropout=self.Dropout, n_shared_block=self.n_shared_block)
        self.shared_G = SharedLayers_G(features=self.n_hidden, n_latent=self.n_latent, Dropout=self.Dropout, n_shared_block=self.n_shared_block)

        self.E1 = Encoder(data_size=self.data_size, n_hidden=self.n_hidden, n_layers=self.n_layers, shared_block=self.shared_E, n_latent=self.n_latent, Dropout=self.Dropout)
        self.E2 = Encoder(data_size=self.data_size, n_hidden=self.n_hidden, n_layers=self.n_layers, shared_block=self.shared_E, n_latent=self.n_latent, Dropout=self.Dropout)
        
        self.G1 = Generator(n_latent=self.n_latent, n_hidden=self.n_hidden, shared_block=self.shared_G, n_layers=self.n_layers, data_size=self.data_size, Dropout=self.Dropout)
        self.G2 = Generator(n_latent=self.n_latent, n_hidden=self.n_hidden, shared_block=self.shared_G, n_layers=self.n_layers, data_size=self.data_size, Dropout=self.Dropout)
        
        # Data Loader for Prediction
        self.data_loader = self.create_data_loader()
        
        if self.KO_mode is True:
            self.data_loader_KO = self.create_data_loader_KO()

        self.load_weights(self.task_name)

        self.E1.to(self.device)
        self.E2.to(self.device)
        self.G1.to(self.device)
        self.G2.to(self.device)

        self.model_initialized = True
            
    def create_data_loader(self):
        class MyDataset(Dataset):
            def __init__(self, adata):
                self.adata = adata.X
                self.num_cells = self.adata.shape[0]
                self.indices = list(range(self.num_cells))
            
            def __len__(self):
                return self.num_cells
            
            def __getitem__(self, idx):
                idx_A = self.indices[idx]
                X1 = self.adata[idx_A]
                return X1
        my_dataset = MyDataset(self.adata)
        return DataLoader(my_dataset, batch_size=self.batch_size, shuffle=False)
    
    def create_data_loader_KO(self):
        class MyDataset(Dataset):
            def __init__(self, adata, indices):
                self.adata = adata.X
                self.indices = indices

            def __len__(self):
                return len(self.indices)

            def __getitem__(self, idx):
                idx_A = self.indices[idx]
                X1 = self.adata[idx_A]
                return X1
        
        # Use the same cell indices as adata for adata_KO
        indices_ko = list(range(len(self.adata)))
        my_dataset_ko = MyDataset(self.adata_KO, indices=indices_ko)
        return DataLoader(my_dataset_ko, batch_size=self.batch_size, shuffle=False)


    # Load pre-trained weights into the model
    def load_weights(self, task_name):
        
        print(f"Loading weights form {task_name}")

        model_weights_path = os.path.join(self.weights_folder, task_name, f"{task_name}_Best_Weights.pth")
        
        if not os.path.exists(model_weights_path):
            raise FileNotFoundError(f"Weights file not found: {model_weights_path}")
        
        state_dict = torch.load(model_weights_path)
        
        E1_weights = state_dict['E1_state_dict']
        E2_weights = state_dict['E2_state_dict']
        G1_weights = state_dict['G1_state_dict']
        G2_weights = state_dict['G2_state_dict']

        self.E1.load_state_dict(E1_weights)
        self.E2.load_state_dict(E2_weights)
        self.G1.load_state_dict(G1_weights)
        self.G2.load_state_dict(G2_weights)

        print("Weight loading completed!")

    def generate_virtual_data(self, model_E, model_G, data_loader, adata, condition_name):
        virtual_data_list = []
        with torch.no_grad():
            for batch in data_loader:
                X = batch.to(self.device)
            
                _, Z = model_E(X, training = False)
                fake_X = model_G(Z, X, training = False)
            
                fake_X = fake_X.detach().cpu().numpy()
                virtual_data_list.append(fake_X)

        mat = np.vstack(virtual_data_list)

        adata_copy = adata.copy()
        adata_copy.X = mat
        adata_copy.obs["Condition"] = condition_name
        current_row_names = adata_copy.obs_names
        new_row_names = [name + "-1" for name in current_row_names]
        adata_copy.obs_names = new_row_names
        adata_copy.obs_names_make_unique()

        return adata_copy

    def Virtual_A2B(self):
        self._initialize_model(force_reload=True)
        self.E1.eval()
        self.G2.eval()
        return self.generate_virtual_data(self.E1, self.G2, self.data_loader, self.adata, "Virtual_A2B")

    def Virtual_B2A(self):
        self._initialize_model(force_reload=True)
        self.E2.eval()
        self.G1.eval()
        return self.generate_virtual_data(self.E2, self.G1, self.data_loader, self.adata, "Virtual_B2A")

    def _virtual_a2b(self, adata):
        self._initialize_model(force_reload=True)
        self.E1.eval()
        self.G2.eval()
        return self.generate_virtual_data(self.E1, self.G2, self.data_loader_KO, adata, "Virtual_KO_A2B")

    def _virtual_b2a(self, adata):
        self._initialize_model(force_reload=True)
        self.E2.eval()
        self.G1.eval()
        return self.generate_virtual_data(self.E2, self.G1, self.data_loader_KO, adata, "Virtual_KO_B2A")

    def Virtual_KO_A2B(self):
        A2B = self.Virtual_A2B()
        KO_A2B = self._virtual_a2b(self.adata_KO)
        merged_adata = ad.concat([A2B, KO_A2B])
        merged_adata.obs_names_make_unique()    
        return merged_adata

    def Virtual_KO_B2A(self):
        B2A = self.Virtual_B2A()
        KO_B2A = self._virtual_b2a(self.adata_KO)
        merged_adata = ad.concat([B2A, KO_B2A])
        merged_adata.obs_names_make_unique()
        return merged_adata
