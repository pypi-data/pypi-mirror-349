from scipy.spatial.distance import jensenshannon
import pandas as pd

class KO_perturbation():
    def __init__(self, adata=None, Condition="A2B"):
        """
        Extracting Virtual Knockout Results.

        Arguments:
        - adata (AnnData, required): An AnnData object obtained through "Virtual_KO_A2B" or "Virtual_KO_B2A".
        - Condition(str, required): Specifies the direction of virtual KO condition transformation. "A2B" or "B2A", default is "A2B".
        """
        self.epsilon = 1e-10
        self.gene_index = adata.var_names
        
        if self.gene_index.empty:
            raise ValueError("Gene index is empty. Please provide a valid adata with gene information.")

        if Condition == "A2B":
            self.V_KO = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_KO_A2B"].X.T)
            self.V = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_A2B"].X.T)
        elif Condition == "B2A":
            self.V_KO = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_KO_B2A"].X.T)
            self.V = pd.DataFrame(adata[adata.obs["Condition"] == "Virtual_B2A"].X.T)
        else:
            raise ValueError("Invalid Condition. Supported values: 'A2B' or 'B2A'.")
        
        self.KO_results = self.calculate_JS_divergence()
        
    def calculate_JS_divergence(self):
        JS_value = pd.DataFrame(index=self.gene_index, columns=['Perturbation_score','Virtual_KO_expression',
                                                                "Virtual_expression","Perturbation_Direction"])
        
        for i, gene in enumerate(self.gene_index):
            
            p_raw = self.V_KO.iloc[i].values
            q_raw = self.V.iloc[i].values

            p = p_raw + self.epsilon
            q = q_raw + self.epsilon
            p = p / p.sum()
            q = q / q.sum()

            js_score = jensenshannon(p, q, base=2)
            
            JS_value.at[gene, 'Perturbation_score'] = js_score
            
            V_KO_mean = p_raw.mean()
            V_mean = q_raw.mean()

            JS_value.at[gene, 'Virtual_KO_expression'] = V_KO_mean
            JS_value.at[gene, 'Virtual_expression'] = V_mean
            
            PD = V_KO_mean - V_mean
            if PD > 0:
                JS_value.at[gene, 'Perturbation_Direction'] = 'Up'
            elif PD < 0:
                JS_value.at[gene, 'Perturbation_Direction'] = 'Down'
            else:
                JS_value.at[gene, 'Perturbation_Direction'] = 'Heterogeneous' if js_score > 0 else 'None'
                
        JS_value.sort_values(by='Perturbation_score', ascending=False, inplace=True)
        
        return JS_value