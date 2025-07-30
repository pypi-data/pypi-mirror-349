import anndata as ad
import numpy as np

class Preparation:
    def __init__(self, 
                 adata = None, 
                 Condition_name = None,
                 Cell_name = None, 
                 Condition_Train = None,
                 Condition_Perturbation = None,
                 Cell_Train = None,
                 Cell_Perturbation = None,
                 KO_mode = True,
                 KO_gene = None,
                 GR = 0.5):
        """
        AnnData Training and Prediction Preprocessing Tool

        Arguments:
        - adata (AnnData, required): An AnnData object.
        - Condition_name (str, required): Column name for perturbation conditions in adata.obs.
        - Cell_name (str, required): Column name for cell types in adata.obs.
        - Condition_Train (list, required): Names of perturbation conditions. Only two conditions can be entered.
        - Cell_Train (list, required): Cell types for training.
        - Condition_Perturbation (list, required): Names of perturbation conditions. Only one condition can be entered.
        - Cell_Perturbation (list, required): Cell types for prediction.
        - K0_mode (Boolean, required): Virtual Knockout Mode. Default: True.
        - KO_gene (list, optional): If K0 mode is True, KO list must be provided.
        - GR (float, optional): Gene Ratio. Sort genes by expression level in descending order to determine the proportion of genes for training, ranging from 0.0 to 1.0, Default: 0.5.
        """
        
        if adata is not None:
            if not isinstance(adata, ad.AnnData):
                raise ValueError("Input data is not an Anndata object.")
            adata.X = adata.X.toarray()
        else:
            raise ValueError("None adata is provided.")
        

        if Condition_name is None or Cell_name is None:
            raise ValueError("Either Condition name or Cell name is not provided.")
        

        if Condition_Train is not None:
            if not isinstance(Condition_Train, list):
                raise ValueError("Condition_Train is not a list.")
            
            if len(Condition_Train) != 2:
                raise ValueError("Condition_Train does not contain exactly 2 elements.")
            
            if Condition_Train[0] == Condition_Train[1]:
                raise ValueError("The two elements in Condition_Train are same.")
        else:
            raise ValueError("None Condition_Train is provided.")

        
        if Cell_Train is not None:
            if not isinstance(Cell_Train, list):
                raise ValueError("Cell_Train is not a list.")
            if len(Cell_Train) >= 2:
                if len(set(Cell_Train)) != len(Cell_Train):
                    raise ValueError("Cell_Train contains duplicate items.")
        else:
            raise ValueError("None cell_Train is provided.")

        if not (isinstance(GR, float) and 0 < GR <= 1):
            raise ValueError("GR is in an invalid numerical range; It should be (0,1].")
        
        if isinstance(KO_mode, bool):
            if KO_mode is True:
                if KO_gene is None:
                    raise ValueError("KO_gene needs to be provided if KO mode is True.")
                elif not isinstance(KO_gene, list):
                    raise ValueError("KO_gene needs to be a list if KO mode is True.")
                elif len(KO_gene) == 0:
                    raise ValueError("KO_gene should not be an empty list if KO mode is True.")
                elif len(set(KO_gene)) != len(KO_gene):
                    raise ValueError("KO_gene contains duplicate items.")
            else:
                pass
        else:
            raise ValueError("KO_mode should be a boolean value.")
        
        self.adata = adata
        self.Cell_type = "Cell_type"
        self.Condition = "Condition"
        self.Condition_name = Condition_name
        self.Cell_name = Cell_name
        self.Condition_Train = Condition_Train
        self.Cell_Train = Cell_Train
        self.Condition_Perturbation = Condition_Perturbation
        self.Cell_Perturbation = Cell_Perturbation
        self.GR = GR
        self.KO_mode = KO_mode
        self.KO_gene = KO_gene
        
    def process_data(self):
        if self.Condition_name is not None and self.Condition_name in self.adata.obs.columns:
            self.adata.obs[self.Condition] = self.adata.obs[self.Condition_name]
        else:
            raise ValueError(f"'{self.Condition_name}' not found in adata.obs.columns")

        
        if self.Cell_name is not None and self.Cell_name in self.adata.obs.columns:
            self.adata.obs[self.Cell_type] = self.adata.obs[self.Cell_name]
        else:
            raise ValueError(f"'{self.Cell_name}' not found in adata.obs.columns")
        
        
        for Condition_value in self.Condition_Train:
            if Condition_value not in self.adata.obs[self.Condition_name].unique():
                raise ValueError(f"'{Condition_value}' is not in '{self.adata.obs[self.Condition_name].unique()}'")
        

        for cell_value in self.Cell_Train:
            if cell_value not in self.adata.obs[self.Cell_name].unique():
                raise ValueError(f"'{cell_value}' is not in '{self.adata.obs[self.Cell_name].unique()}'")
        
        
        if self.Condition_Perturbation is not None:
            if not isinstance(self.Condition_Perturbation, list):
                raise ValueError("Condition perturbation is not a list.")
            
            if len(self.Condition_Perturbation) != 1:
                raise ValueError("Condition perturbation does not contain exactly 1 elements.")
            
            if self.Condition_Perturbation[0] not in self.Condition_Train:
                raise ValueError("Condition perturbation should be in Condition_Train.")
        else:
            raise ValueError("None Condition perturbation is provided.")
        
        self.adata_Perturbation = self.adata[self.adata.obs[self.Condition_name].isin(self.Condition_Perturbation)]
        
        
        if self.Cell_Perturbation is not None:
            if not isinstance(self.Cell_Perturbation, list):
                raise ValueError("Cell perturbation is not a list.")
                
            if len(self.Cell_Perturbation) >= 2:
                if len(set(self.Cell_Perturbation)) != len(self.Cell_Perturbation):
                    raise ValueError("Cell perturbation contains duplicate items.")
                    
            for value in self.Cell_Perturbation:
                if value not in self.adata.obs[self.Cell_type].values:
                    raise ValueError(f"'{value}' not found in {self.adata.obs[self.Cell_type].values}")
        else:
            raise ValueError("None cell perturbation is provided.")
        
        self.adata_Perturbation = self.adata_Perturbation[self.adata_Perturbation.obs[self.Cell_name].isin(self.Cell_Perturbation)]

        self.adata_Train = self.adata[self.adata.obs[self.Condition_name].isin(self.Condition_Train)]
        self.adata_Train = self.adata_Train[self.adata_Train.obs[self.Cell_name].isin(self.Cell_Train)]
        del self.adata
        
        gene_expression_mean = np.mean(self.adata_Perturbation.X, axis=0)
        sorted_genes = np.argsort(gene_expression_mean)[::-1]
        num_selected_genes = int(len(sorted_genes) * self.GR)
        print(f"The number of genes selected was {num_selected_genes}.")
        
        selected_genes = sorted_genes[:num_selected_genes].flatten()
        exp_gene = self.adata_Perturbation[:, selected_genes].var_names
        
        self.adata_Train = self.adata_Train[:, exp_gene].copy()
        self.adata_Train = ad.AnnData(self.adata_Train)

        if self.KO_mode is False:
            self.adata_Perturbation = self.adata_Perturbation[:, exp_gene].copy()
            self.adata_Perturbation = ad.AnnData(self.adata_Perturbation)
        else:
            self.adata_Perturbation = self.adata_Perturbation[:, exp_gene].copy()
            self.adata_Perturbation_KO = self.adata_Perturbation[:, exp_gene].copy()
            for gene in self.KO_gene:
                if gene not in exp_gene:
                    raise ValueError(f"KO gene:'{gene}' is not in the top {self.GR*100}% of expressed genes.")
                else:
                    self.gene_index = self.adata_Perturbation_KO.var_names.get_loc(gene)
                    self.adata_Perturbation_KO.X[:, self.gene_index] = 0
                    
            self.adata_Perturbation = ad.AnnData(self.adata_Perturbation)
            self.adata_Perturbation_KO = ad.AnnData(self.adata_Perturbation_KO)