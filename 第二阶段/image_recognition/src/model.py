import torch.nn as nn
from torch.nn import ReLU


class ImagenetModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(3, 16, 3, padding=1),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # 128 -> 64
            nn.Conv2d(16, 32, 3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # 64 -> 32
            nn.Conv2d(32, 64, 3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2, 2),
            # 32 -> 16
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1,1)),
            nn.Flatten(),
            nn.Dropout(0.4),
            # 第一个参数 = 输入维度，必须等于上一层的通道数（这里是 64）
            # 第二个参数 = 这一层输出的维度（想多宽写多宽）
            nn.Linear(64, 32),
            ReLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x.squeeze(dim=1)

if __name__ == "__main__":
    import torch
    model = ImagenetModel()
    x = torch.ones(1, 3, 224, 224)
    y = model(x)
    print(f"输入 {tuple(x.shape)} → 输出 {tuple(y.shape)}")