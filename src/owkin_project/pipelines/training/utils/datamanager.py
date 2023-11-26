from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader

class MILDataset(Dataset):
    """
    Class for MIL dataset. Each observation from the dataset, called "bag" contains n_instances instances of dim = n_features.
    
    Args:
        - X (np.array): array of shape (n_bags * n_instances, n_features) containing the features of each instance in the bagq
        - y (np.array): if not None, array of shape (n_bags * n_instances, ) containing the target of each bag
        - n_instances (int): number of instances per bag
        - scaler (sklearn.preprocessing): scaler to apply to the features
    """
    def __init__(self, X, y = None, n_instances = 1000, scaler = None):
        n_bags, n_features = len(X)//n_instances, X.shape[-1]
        self.n_instances = n_instances
        self.scaler = scaler
        if scaler is not None:
            X = scaler.transform(X)
        self.X = X.reshape(n_bags, n_instances, n_features) # create n bags of 1000 instances of dim = n_features
        self.y = y 
            
    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        features = self.X[idx,:,:]
        target = None
        if self.y is not None:
            target = float(self.y[idx*self.n_instances]) # bag label is the label of the first instance of the bag
        return features, target 

class InstanceDataset(Dataset):
    """
    Class for Instance dataset. Each observation from the dataset contains one instance of dim = n_features.
    
    Args:
        - X (np.array): array of shape (n_bags * n_instances, n_features) containing the features of each instance
        - y (np.array): if not None, array of shape (n_bags * n_instances, ) containing the target of each instance
    """
    def __init__(self, X, y = None):
        self.X = X
        self.y = y 
            
    def __len__(self):
        return len(self.X)

    def __getitem__(self, idx):
        features = self.X[idx,:]
        target = None
        if self.y is not None:
            target = float(self.y[idx])
        return features, target 

def get_MILDataset(X, y = None, n_instances: int = 1000, scaler = None) -> MILDataset:   
    dataset = MILDataset(X, y, n_instances, scaler)
    return dataset

def get_InstanceDataset(X, y = None) -> MILDataset:   
    dataset = InstanceDataset(X, y)
    return dataset

def get_dataloader(dataset, batch_size: int, shuffle: bool = True) -> DataLoader:
    data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
    return data_loader
