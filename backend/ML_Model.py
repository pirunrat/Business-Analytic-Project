from joblib import load
import seaborn as sns
import numpy as np
import pandas as pd

class Model:

    def __init__(self,model_path):
        self.model = load(model_path)
        
    def load(self, model_path):
        try:
            loaded_model = load(model_path)
        except KeyError as e:
            return f'Error from loading the model : {e}'
        return loaded_model
    
    def predict(self, newData):
        try:
            result = self.model.predict(newData)
        except KeyError as e:
            return f'Error from prediction function : {e}'
        
        return result
    