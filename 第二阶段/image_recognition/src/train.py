import time
from pathlib import Path

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import torch
import torch.nn as nn

from dataset import build_loader
from model import ImagenetModel

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT/ "output"
OUT.mkdir(parents=True, exist_ok=True)

EPOCHES = 100
LR =5e-4
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

def train_one_epoch(model,optimizer,device,criterion,train_loader):
    model.train()
    total,loss_sum,correct = 0,0.0,0
    for images,labels in train_loader:
        images,labels = images.to(device),labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs,labels)
        loss.backward()
        optimizer.step()
        loss_sum += loss.item()*labels.size(0)
        pred = (torch.sigmoid(outputs)>0.5).float()
        # True/False 转为 1/0
        correct += (pred == labels).sum().item()
        # .item() 转为普通数字
        total += labels.size(0)
    return loss_sum/total,correct/total

@torch.no_grad()
def evaluate(model,device,criterion,test_loader):
    model.eval()
    total,loss_sum,correct = 0,0.0,0
    for images,labels in test_loader:
        images,labels = images.to(device),labels.to(device)
        outputs = model(images)
        loss = criterion(outputs,labels)
        loss_sum += loss.item()*labels.size(0)
        pred = (torch.sigmoid(outputs)>0.5).float()
        correct += (pred == labels).sum().item()
        total += labels.size(0)
    return loss_sum/total,correct/total

def main():
    torch.manual_seed(42)
    print(f"设备:{DEVICE}")

    train_loader, val_loader, _ = build_loader()
    model = ImagenetModel().to(DEVICE)
    print(f"参数: {sum(p.numel() for p in model.parameters()):,}")
    print(f"训练 {len(train_loader.dataset)}张 | 验证 {len(val_loader.dataset)}张")
    criterion = nn.BCEWithLogitsLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=LR, weight_decay=5e-4)

    history = {"train_loss": [], "train_acc": [], "val_loss": [], "val_acc": []}

    best_acc = 0.0
    t0 = time.time()
    for epoch in range(1,EPOCHES+1):
        tr_loss, tr_acc = train_one_epoch(model,optimizer,DEVICE,criterion,train_loader)
        val_loss, val_acc = evaluate(model,DEVICE,criterion,val_loader)

        for k, v in zip(("train_loss", "train_acc", "val_loss", "val_acc"),
                        (tr_loss, tr_acc, val_loss, val_acc)):
            history[k].append(v)

        flag = ""
        if val_acc > best_acc:
            best_acc = val_acc
            torch.save(model.state_dict(),OUT/"best.pt")
            flag = " <- 保存"
        print(f"epoch {epoch:2d} | 训练 {tr_loss:.4f}/{tr_acc:.4f} | "
              f"验证 {val_loss:.4f}/{val_acc:.4f} | {flag}")
    print(f"\n训练耗时 {time.time() - t0:.1f} 秒，最佳验证准确率 {best_acc:.4f}")
    # 画曲线图
    epochs = range(1,len(history["train_loss"])+1)
    fig, axes = plt.subplots(1, 2, figsize=(11,4))
    axes[0].plot(epochs, history["train_loss"], marker="o", label="训练")
    axes[0].plot(epochs, history["val_loss"], marker="o", label="验证")
    axes[0].set_title("损失 loss")
    axes[0].set_xlabel("epoch")
    axes[0].legend()  # 显示图例
    axes[0].grid(alpha=0.3)  # 画淡网格，方便读数

    axes[1].plot(epochs, history["train_acc"], marker="o", label="训练")
    axes[1].plot(epochs, history["val_acc"], marker="o", label="验证")
    axes[1].set_title("准确率 accuracy")
    axes[1].set_xlabel("epoch")
    axes[1].legend()
    axes[1].grid(alpha=0.3)

    fig.tight_layout()  # 自动调整间距，防止标题被裁掉
    fig.savefig(OUT / "curves.png", dpi=150)  # dpi 越高越清晰，文件也越大
    plt.close(fig)

    print(f"曲线已保存：{OUT / 'curves.png'}")

if __name__ == "__main__":
    main()
