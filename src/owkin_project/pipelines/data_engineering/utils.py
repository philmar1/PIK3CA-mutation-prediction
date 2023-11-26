import numpy as np
from sklearn.preprocessing import StandardScaler

import logging
logger = logging.getLogger(__name__)

class CenterStandardScaler():
    def __init__(self) -> None:
        self.scalers = {}
        self.all_centers = []
        
    def fit(self, X, indexs):
        """ Fit Scaler for each of the center 

        Args:
            X (n_slices, n_features): features for each slice
            indexs (n_slices, 3): indexs of each slice : (personID, sliceID, centerID)
        """
        self.all_centers = np.unique(indexs[:,-1]).tolist()
        self.scalers = {centerID: StandardScaler() for centerID in self.all_centers}
        for centerID in self.all_centers:
            center_mask = (indexs[:,-1] == centerID)
            X_masked = X[center_mask]
            self.scalers[centerID].fit(X_masked)
            
        logger.info('Fitted X for centers: {}'.format(self.all_centers))
            
    def transform(self, X, indexs):
        """ Use fitted scalers to transform new data. If new center is encountered,
        fit a new scaler

        Args:
            X (n_slices, n_features): features for each slice
            indexs (n_slices, 3): indexs of each slice : (personID, sliceID, centerID)
        """
        old_centers = self.all_centers.copy()
        all_centers = np.unique(indexs[:,-1]).tolist()
        new_centers = [centerID for centerID in all_centers if centerID not in old_centers]
        for centerID in all_centers:
            center_mask = (indexs[:,-1] == centerID)
            X_masked = X[center_mask]
            if centerID in self.all_centers:    
                X_masked = self.scalers[centerID].transform(X_masked)
            else:
                self.scalers[centerID] = StandardScaler()
                self.scalers[centerID].fit(X_masked)
                X_masked = self.scalers[centerID].transform(X_masked)
            X[center_mask] = X_masked    
        logger.info('Transformed X for centers: {}, find new centers:{}'.format(old_centers, new_centers))
        return X