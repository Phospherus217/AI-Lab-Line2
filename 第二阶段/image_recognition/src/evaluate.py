from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import torch

from dataset import build_loader
from model import ImagenetModel

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'output'
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
CLASSES = ["其他","登录页"]

@torch.no_grad()
def evaluate(model, loader, device):
    model.eval()
    all_labels = []
    all_pred = []
    all_images = []
    all_probs = []
    for images, labels in loader:
        images = images.to(device)
        labels = labels.to(device)
        outputs = model(images)
        prob = torch.sigmoid(outputs)
        pred = (prob > 0.5).float()
        all_labels.append(labels)
        all_pred.append(pred)
        all_images.append(images)
        all_probs.append(prob)
        # 变为1/0
    return (torch.cat(all_pred,dim=0), torch.cat(all_labels,dim=0),
            torch.cat(all_images,dim=0), torch.cat(all_probs,dim=0))

def main():
    _,_,test_loader = build_loader()
    model = ImagenetModel().to(DEVICE)
    model.load_state_dict(torch.load(ROOT / "output" / "best.pt", map_location = DEVICE))
    pred,labels,images,probs = evaluate(model, test_loader, DEVICE)
    tp = fp = fn =tn = 0
    wrong = []
    for i in range(len(labels)):
        t, p = int(labels[i]), int(pred[i])
        if t == 1 and p == 1:          # 真1 判1 → 判对
            tp += 1
        elif t == 0 and p == 1:        # 真0 判1 → 误报
            fp += 1
        elif t == 1 and p == 0:        # 真1 判0 → 漏报
            fn += 1
        else:                          # 真0 判0 → 判对
            tn += 1

        if t != p:
            wrong.append((images[i].cpu(), t, p, float(probs[i])))

    total = tp + tn + fp + fn
    accuracy = (tp + tn)/total
    recall = tp/(tp+fn) if (tp+fn) else 0.0
    precision = tp/(tp+fp) if (tp+fp) else 0.0

    print(f"  测试集 {total} 张")
    print(f"  准确率 accuracy : {accuracy:.4f}")
    print(f"  精确率 precision: {precision:.4f}")
    print(f"  召回率 recall   : {recall:.4f}")
    print(f"  tp={tp} fp={fp} fn={fn} tn={tn}")

    # 存文件
    with open(ROOT / "output" / "report.txt", "w", encoding = "utf-8") as f:
        test = (f"判对:{tp + tn}\n"
                f"误报:{fp}\n"
                f"漏报:{fn}\n"
                f"测试集 {total} 张\n"
                f"准确率 accuracy : {accuracy:.4f}\n"
                f"精确率 precision: {precision:.4f}\n"
                f"召回率 recall   : {recall:.4f}")
        f.write(test)
        print(f"已写入{ROOT / "output" / "report"}")

    # 混淆矩阵：行 = 真实，列 = 预测
    cm = [[tn, fp], [fn, tp]]
    fig, ax = plt.subplots(figsize=(5,4))
    ax.imshow(cm, cmap="Greens", origin="lower")
    ax.set_xticks([0,1], ["other","login"])
    ax.set_yticks([0,1], ["other","login"])
    ax.set_xlabel("真实")
    ax.set_ylabel("预测")
    ax.set_title("混淆矩阵")
    cm_max = max(max(r) for r in cm)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i][j], ha="center", va="center",
                    color="white" if cm[i][j] > cm_max / 2 else "black", fontsize = 13)
    fig.tight_layout()
    fig.savefig(ROOT / "output" / "confusion_matrix.png", dpi = 150)
    plt.close(fig)
    print(f"混淆矩阵已保存：{ROOT / "output" / "confusion_matrix.png"}")

    # ---- 把错例画成 2×4 的网格 ----
    if wrong:
        fig, axes = plt.subplots(2, 4, figsize=(14, 7))
        for ax, (img, t, p, prob) in zip(axes.flat, wrong[:8]):
            disp = img.permute(1, 2, 0).numpy()
            disp = (disp - disp.min()) / (disp.max() - disp.min() + 1e-8)
            ax.imshow(disp)
            ax.set_title(f"真实 {CLASSES[t]} / 预测 {CLASSES[p]}\n置信度 {prob:.2f}", fontsize=10)
            ax.axis("off")
        for ax in axes.flat[len(wrong[:8]):]:   # 没填满的格子也关掉坐标轴
            ax.axis("off")
        fig.tight_layout()
        fig.savefig(OUT / "error_cases.png", dpi=150)
        plt.close(fig)
        print(f"错例已保存：{OUT / 'error_cases.png'}（共 {len(wrong)} 个）")
    else:
        print("没有错例，跳过画错例图")
if __name__ == "__main__":
    main()