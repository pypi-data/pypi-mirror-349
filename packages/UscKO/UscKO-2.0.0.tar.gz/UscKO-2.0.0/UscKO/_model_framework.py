import math
import torch

import torch.nn as nn
import torch.nn.functional as F

from torch.distributions import Distribution, constraints, Normal, Gamma, Poisson as PoissonTorch
from torch.distributions.utils import broadcast_all, logits_to_probs

from typing import Optional, Union

######################
# shared_block E
######################
class SharedLayers_E(nn.Module):
    def __init__(self, n_shared_block=1, features=None, n_latent=None, Dropout=0.1):
        super(SharedLayers_E, self).__init__()
        
        layers = []
        for _ in range(n_shared_block):
            layers += [
                nn.Linear(features, features),
                nn.BatchNorm1d(features),
                nn.GELU(),
                nn.Dropout(Dropout),
            ]
        self.Shared = nn.Sequential(*layers).float()
        
        self.mean = nn.Linear(features, n_latent)
        self.var = nn.Linear(features, n_latent)
    
    def forward(self, x):
        x = self.Shared(x.float())
        
        z_m = self.mean(x)
        z_var = self.var(x)
        
        return z_m, z_var

######################
# shared_block G
######################
class SharedLayers_G(nn.Module):
    def __init__(self, n_shared_block=1, features=None, n_latent=None, Dropout=0.1):
        super(SharedLayers_G, self).__init__()
        
        layers = []
        layers += [
            nn.Linear(n_latent, features),
            nn.BatchNorm1d(features),
            nn.GELU(),
            nn.Dropout(Dropout),
        ] 
        for _ in range(n_shared_block - 1):
            layers += [
                nn.Linear(features, features),
                nn.BatchNorm1d(features),
                nn.GELU(),
                nn.Dropout(Dropout),
            ]
        self.Shared = nn.Sequential(*layers).float()
    
    def forward(self, x):
        x = self.Shared(x.float())
        return x

#########################
# Encoder
#########################
class Encoder(nn.Module):
    def __init__(self, data_size=None, n_hidden=256, n_latent=128, n_layers=3, shared_block=None, Dropout=0.1):
        super(Encoder, self).__init__()

        layers = []  
        layers += [
            nn.Linear(data_size, n_hidden),
            nn.BatchNorm1d(n_hidden),
            nn.GELU(),
            nn.Dropout(Dropout),
        ]
        for _ in range(n_layers - 1):
            layers += [
                nn.Linear(n_hidden, n_hidden),
                nn.BatchNorm1d(n_hidden),
                nn.GELU(),
                nn.Dropout(Dropout),
            ]
            
        self.model_blocks = nn.Sequential(*layers).float()
        self.shared_block = shared_block

    def forward(self, x, training=True):
        x = self.model_blocks(x.float())
        z_mu, z_log_var = self.shared_block(x)
        z_log_var = torch.clamp(z_log_var, min=-15, max=15)
        
        z_std = torch.exp(z_log_var/2) # log var
        dist = Normal(z_mu, z_std)
        
        if training:
            eps = torch.randn_like(z_std)
            z = z_mu + eps * z_std
        else:
            z = z_mu
        return dist, z

#########################
# Generator
#########################
class ZINB(Distribution):
    
    support = constraints.nonnegative_integer
    has_rsample = True
    arg_constraints = {}

    def __init__(self, mu, theta, zi_logits, eps=1e-8):
        
        self.zi_logits, self.mu, self.theta = broadcast_all(zi_logits, mu, theta)
        self.eps=eps
        super().__init__() 
    
    def zi_probs(self):
        return logits_to_probs(self.zi_logits, is_binary=True)
    
    def log_prob(self, value):

        mu, theta, pi = self.mu, self.theta, self.zi_logits
        eps = self.eps
        log_theta = torch.log(theta + eps)
        log_mu_theta = torch.log(theta + mu + eps)
        
        softplus_pi = F.softplus(-pi)
        pi_theta_log = -pi + theta * (log_theta - log_mu_theta)
        
        case_zero = F.softplus(pi_theta_log) - softplus_pi
        case_non_zero = (
            -softplus_pi
            + pi_theta_log
            + value * (torch.log(mu + eps) - log_mu_theta)
            + torch.lgamma(value + theta)
            - torch.lgamma(theta)
            - torch.lgamma(value + 1)
        )
        
        res = torch.where(value < eps, case_zero, case_non_zero)
        return res
    
    def rsample(self, sample_shape=torch.Size()):

        gamma_d = Gamma(self.theta, self.theta / (self.mu.clamp(min=self.eps)))
        p_means = gamma_d.rsample(sample_shape)
        p_means = torch.clamp(p_means, min=1e-8, max=1e8)
        
        with torch.no_grad():
            counts = PoissonTorch(p_means).sample()
            zero_mask = torch.rand_like(counts) < self.zi_probs()
            samp = torch.where(zero_mask, torch.zeros_like(counts), counts)

        return samp

class Decoder_G(nn.Module):
    def __init__(self, data_size=None, n_hidden = 256, n_latent=128, n_layers=3, shared_block=None, Dropout=0.1):
        super().__init__()
        
        self.shared_block = shared_block
        
        layers = [
            nn.Linear(n_hidden, n_hidden),
            nn.BatchNorm1d(n_hidden),
            nn.GELU(),
            nn.Dropout(Dropout),
        ]
        for _ in range(n_layers - 1):
            layers += [
                nn.Linear(n_hidden, n_hidden),
                nn.BatchNorm1d(n_hidden),
                nn.GELU(),
                nn.Dropout(Dropout),
            ]
        self.model_blocks = nn.Sequential(*layers).float()
        
        
        self.decoder_mu = nn.Sequential(nn.Linear(n_hidden, data_size), nn.Softmax(dim=-1))
        self.decoder_theta = nn.Sequential(nn.Linear(n_hidden, data_size), nn.Softplus())
        self.decoder_dropout = nn.Linear(n_hidden, data_size)

    def forward(self, z, x): 

        library = torch.log(x.sum(1)).unsqueeze(1)
        px = self.shared_block(z)
        px = self.model_blocks(px)
        
        mu = self.decoder_mu(px) * torch.exp(library)
        theta = self.decoder_theta(px)
        zi_logits = self.decoder_dropout(px)

        return mu, theta, zi_logits

class Generator(nn.Module):
    def __init__(self, data_size=None, n_hidden=256, n_latent=128, n_layers=3, shared_block=None, Dropout=0.1):
        super().__init__()
        
        self.Decoder_G = Decoder_G(data_size=data_size, 
                                   n_hidden=n_hidden,
                                   n_latent=n_latent, 
                                   shared_block=shared_block,
                                   n_layers=n_layers,
                                   Dropout=Dropout)

    def forward(self, z, x, training=True):

        mu, theta, zi_logits = self.Decoder_G(z, x)
        zinb_dist = ZINB(mu=mu, theta=theta, zi_logits=zi_logits)

        if training:
            log_prob = zinb_dist.log_prob(x)
            return mu, log_prob
        else:
            sample = zinb_dist.rsample()
            return sample

#########################
# Discriminator
#########################
class Discriminator(nn.Module):
    def __init__(self, data_size=None, n_hidden=256, n_layers_D=2, Dropout=0.1):
        super(Discriminator, self).__init__()
        
        layers = []
        layers += [nn.Linear(data_size, n_hidden),
                   nn.LayerNorm(n_hidden),
                   nn.GELU(),
                   nn.Dropout(Dropout)
                  ]
        for _ in range(n_layers_D - 1):
            layers += [
                nn.Linear(n_hidden, n_hidden),
                nn.LayerNorm(n_hidden),
                nn.GELU(),
                nn.Dropout(Dropout),
            ] 
        layers += [
            nn.Linear(n_hidden, 1),
        ]
        
        self.model_blocks = nn.Sequential(*layers)
        
    def forward(self, x):
        out = self.model_blocks(x.float())
        return out.float()

#########################
# Initialization weights
#########################
def init_weights(m):
    classname = m.__class__.__name__
    
    if classname.find("Linear") != -1:
        nn.init.xavier_normal_(m.weight)
        if m.bias is not None:
            nn.init.constant_(m.bias, 0.0)
    
    elif classname.find("BatchNorm1d") != -1:
        nn.init.constant_(m.weight, 1.0)
        nn.init.constant_(m.bias, 0.0)

    elif classname.find("LayerNorm") != -1:
        nn.init.constant_(m.weight, 1.0)
        nn.init.constant_(m.bias, 0.0)

#########################
# Learning Rate Scheduler
#########################
class LambdaLR2:
    def __init__(self, n_epochs, decay_start_epoch):
        assert (n_epochs - decay_start_epoch) > 0, "Decay must start before the training session ends!"
        self.n_epochs = n_epochs
        self.decay_start_epoch = decay_start_epoch
        
    def step(self, epoch):
        return 1.0 - max(0, epoch - self.decay_start_epoch) / (self.n_epochs - self.decay_start_epoch)