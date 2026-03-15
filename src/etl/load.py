import torch
from torch.utils.data import Dataset, DataLoader

class BridgeDefectDataset(Dataset):
    def __init__(self, sequences, labels):
        self.sequences = torch.FloatTensor(sequences).permute(0, 1, 4, 2, 3) 
        self.labels = torch.FloatTensor(labels)

    def __len__(self): return len(self.sequences)
    def __getitem__(self, idx): return self.sequences[idx], self.labels[idx]
