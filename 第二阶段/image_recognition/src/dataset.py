from pathlib import Path

import torch
from torch.utils.data import Dataset ,DataLoader

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "data" / "gui_cache.pt"

MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]

class ImageDataset(Dataset):
    def __init__(self,x,y,augment=False):
        super().__init__()
        # augment:数据增强
        self.x = x
        self.y = y
        self.augment = augment
    def __len__(self):
        return len(self.x)
    def __getitem__(self, idx):
        img = self.x[idx].float()/255.0
        for c in range(3):
            img[c] = (img[c] - MEAN[c]) / STD[c]
        if self.augment and torch.rand(1) > 0.5:
            img = torch.flip(img, dims = [2])
        return img, self.y[idx]

def build_loader(batch_size=32,val_ratio=0.1,test_ratio=0.1,seed=42):
    data = torch.load(CACHE)
    x, y = data['x'], data['y']

    total =len(x)
    n_val = max(1,int(total*val_ratio))
    n_test = max(1,int(total*test_ratio))
    n_train = total - n_val - n_test
    g = torch.Generator().manual_seed(seed)
    perm = torch.randperm(total,generator=g)
    x = x[perm]
    y = y[perm]
    train_set = ImageDataset(x[:n_train],y[:n_train],augment=True)
    val_set = ImageDataset(x[n_train:n_val+n_train],y[n_train:n_val+n_train],augment=False)
    test_set = ImageDataset(x[n_val+n_train:],y[n_val+n_train:],augment=False)
    train_loader = DataLoader(train_set,batch_size=batch_size,shuffle=True,num_workers=0)
    val_loader = DataLoader(val_set,batch_size=batch_size,shuffle=False,num_workers=0)
    test_loader = DataLoader(test_set,batch_size=batch_size,shuffle=False,num_workers=0)
    return train_loader,val_loader,test_loader

if __name__ == "__main__":
    train_loader,_,_ = build_loader()
    images,labels = next(iter(train_loader))
    print("batch1")
    print(f"image{tuple(images.shape)} {images.dtype}")
    print(f"label{tuple(labels.shape)} {labels.dtype}")
    print(f"像素范围: {images.min():.2f}~{images.max():.2f}")
    print(f"均值: {images.mean():.3f}")