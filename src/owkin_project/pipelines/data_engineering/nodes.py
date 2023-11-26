"""
This is a boilerplate pipeline 'data_engineering'
generated using Kedro 0.18.14
"""
import numpy as np
from .utils import CenterStandardScaler

import logging

logger = logging.getLogger(__name__)

def get_train_eval_IDs(metadata, eval_pct: float = 0.33):
    # keep only patientID and center to split train and eval sets
    IDs = metadata[['Patient ID','Center ID']].drop_duplicates().values
    n = len(IDs)
    
    # Get train IDs
    selected_IDs = np.random.randint(0, n, int(eval_pct * n))
    eval_IDs = IDs[selected_IDs] 
    train_IDs = np.delete(IDs, selected_IDs, axis=0)
    
    return eval_IDs, train_IDs    

def split_train_eval(data, indexs, eval_IDs, train_IDs):
    # Get train indexs
    train_indexs = np.isin(indexs[:,[0,2]], train_IDs).min(axis=1)
    eval_indexs = np.isin(indexs[:,[0,2]], eval_IDs).min(axis=1)
    
    data_train, data_eval = data[train_indexs], data[eval_indexs]
    
    return data_train, data_eval

def shuffleX(X):
    n = 1000
    n_features = X.shape[-1]
    return X
 
def scale(X, indexs, scaler = None):
    if scaler is None:
        scaler = CenterStandardScaler()
        scaler.fit(X, indexs)
        return scaler, scaler.transform(X, indexs)
    return scaler.transform(X, indexs)
    
def fit_scaler(X, indexs):
    scaler = CenterStandardScaler()
    scaler.fit(X, indexs)
    return scaler