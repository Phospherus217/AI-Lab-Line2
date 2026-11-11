"""Post-training analysis: validation-set error cases, per-class accuracy, confusion matrix.

Runs after 01/02/03 have produced state_dicts. Writes CSV/JSON/PNG into results/.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import torch
import torch.nn as nn

ROOT = Path(r"C:\Users\30779\.dsh\dsh_orb\lab_stage1\AI-Lab_Line2_DL_Stage1_Package")
DATA_DIR = ROOT / "data"
RESULTS_DIR = ROOT / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
BATCH_SIZE = 128

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

CLASS_NAMES = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
               "Sandal", "Shirt", "Sneaker", "Bag", "Ankle boot"]
CLASS_CN = ["T恤/上衣", "裤子", "套头衫", "连衣裙", "外套",
            "凉鞋", "衬衫", "运动鞋", "包", "短靴"]


class MLP(nn.Module):
    def __init__(self):
        super().__init__()
        self.network = nn.Sequential(
            nn.Flatten(), nn.Linear(28 * 28, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(), nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.network(x)


class CNN(nn.Module):
    def __init__(self, channels_1=32, channels_2=64, kernel_size=3):
        super().__init__()
        padding = kernel_size // 2
        self.features = nn.Sequential(
            nn.Conv2d(1, channels_1, kernel_size=kernel_size, padding=padding),
            nn.ReLU(), nn.MaxPool2d(2),
            nn.Conv2d(channels_1, channels_2, kernel_size=kernel_size, padding=padding),
            nn.ReLU(), nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.Flatten(), nn.Linear(channels_2 * 7 * 7, 128), nn.ReLU(), nn.Linear(128, 10),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


def build_val_split():
    from torchvision import datasets, transforms
    from torch.utils.data import random_split
    full = datasets.FashionMNIST(root=str(DATA_DIR), train=True, download=False,
                                 transform=transforms.ToTensor())
    train_ds, val_ds = random_split(
        full, [55000, 5000], generator=torch.Generator().manual_seed(SEED))
    return full, train_ds, val_ds


def predict(model, dataset, batch_size=BATCH_SIZE):
    loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)
    model.eval()
    probs_all, preds_all, labels_all = [], [], []
    with torch.no_grad():
        for images, labels in loader:
            logits = model(images)
            probs = torch.softmax(logits, dim=1)
            probs_all.append(probs)
            preds_all.append(probs.argmax(dim=1))
            labels_all.append(labels)
    return (torch.cat(probs_all), torch.cat(preds_all), torch.cat(labels_all))


ARCH = {
    "mlp_baseline": ("mlp", {}),
    "mlp_lr_variant_0p0003": ("mlp", {}),
    "cnn_baseline": ("cnn", {"channels_1": 32, "channels_2": 64, "kernel_size": 3}),
    "cnn_structure_variant": ("cnn", {"channels_1": 16, "channels_2": 32, "kernel_size": 3}),
    "cnn_learning_rate_study_0p0001": ("cnn", {"channels_1": 32, "channels_2": 64, "kernel_size": 3}),
    "cnn_learning_rate_study_0p001": ("cnn", {"channels_1": 32, "channels_2": 64, "kernel_size": 3}),
    "cnn_learning_rate_study_0p01": ("cnn", {"channels_1": 32, "channels_2": 64, "kernel_size": 3}),
}


def model_from_checkpoint(state_name):
    kind, kwargs = ARCH[state_name]
    model = CNN(**kwargs) if kind == "cnn" else MLP()
    state = torch.load(RESULTS_DIR / f"{state_name}_state_dict.pt", map_location="cpu")
    model.load_state_dict(state)
    return model


def main():
    full, train_ds, val_ds = build_val_split()
    val_indices = np.array(val_ds.indices)
    print(f"val size={len(val_ds)}, first global indices={val_indices[:5]}")

    summary = {}
    per_class_rows = []
    for name in ARCH:
        ckpt = RESULTS_DIR / f"{name}_state_dict.pt"
        if not ckpt.exists():
            print("skip", name)
            continue
        model = model_from_checkpoint(name)
        probs, preds, labels = predict(model, val_ds)
        acc = (preds == labels).float().mean().item() * 100
        summary[name] = {"val_accuracy_pct": round(acc, 2),
                         "n": int(len(labels)),
                         "n_wrong": int((preds != labels).sum().item())}
        for c in range(10):
            mask = labels == c
            per_class_rows.append({
                "model": name, "class_id": c, "class": CLASS_NAMES[c],
                "n": int(mask.sum()),
                "accuracy_pct": round((preds[mask] == labels[mask]).float().mean().item() * 100, 2),
            })
        if name == "cnn_baseline":
            cnn_probs, cnn_preds, cnn_labels = probs, preds, labels

    pd.DataFrame(per_class_rows).to_csv(
        RESULTS_DIR / "validation_per_class_accuracy.csv", index=False, encoding="utf-8-sig")
    (RESULTS_DIR / "validation_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    # ---- CNN validation error cases with dataset indices
    wrong = (cnn_preds != cnn_labels).nonzero(as_tuple=True)[0].tolist()
    conf = cnn_probs.max(dim=1).values
    rows = []
    for i in wrong[:10]:
        rows.append({
            "val_position": i,
            "dataset_index": int(val_indices[i]),
            "true_id": int(cnn_labels[i]),
            "true_class": CLASS_NAMES[int(cnn_labels[i])],
            "pred_id": int(cnn_preds[i]),
            "pred_class": CLASS_NAMES[int(cnn_preds[i])],
            "pred_confidence": round(float(conf[i]), 4),
        })
    err_df = pd.DataFrame(rows)
    err_df.to_csv(RESULTS_DIR / "cnn_validation_error_cases.csv", index=False, encoding="utf-8-sig")
    print(err_df.to_string(index=False))

    fig, axes = plt.subplots(2, 5, figsize=(13, 5.6))
    for ax in axes.flat:
        ax.axis("off")
    for ax, row in zip(axes.flat, rows):
        img, _ = full[row["dataset_index"]]
        ax.imshow(img.squeeze(0), cmap="gray")
        ax.set_title(
            f"#{row['dataset_index']} 真实:{CLASS_CN[row['true_id']]}\n"
            f"预测:{CLASS_CN[row['pred_id']]} (置信度 {row['pred_confidence']:.2f})",
            fontsize=8,
        )
        ax.axis("off")
    fig.suptitle("CNN 基线在验证集上的前 10 个错误预测（样本编号为 Fashion-MNIST 训练集全局索引）")
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "cnn_validation_error_cases_analysis.png", dpi=150)
    print("saved", RESULTS_DIR / "cnn_validation_error_cases_analysis.png")

    # ---- confusion matrix for the CNN baseline
    cm = np.zeros((10, 10), dtype=int)
    for t, p in zip(cnn_labels.tolist(), cnn_preds.tolist()):
        cm[t, p] += 1
    cm_df = pd.DataFrame(cm, index=[f"{i}:{n}" for i, n in enumerate(CLASS_NAMES)],
                         columns=[f"{i}:{n}" for i, n in enumerate(CLASS_NAMES)])
    col_order = list(cm_df.columns)
    cm_df.to_csv(RESULTS_DIR / "cnn_validation_confusion_matrix.csv", encoding="utf-8-sig")
    fig, ax = plt.subplots(figsize=(8.5, 7.5))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(10)); ax.set_yticks(range(10))
    ax.set_xticklabels(col_order, rotation=90, fontsize=7)
    ax.set_yticklabels(col_order, fontsize=7)
    ax.set_xlabel("Predicted"); ax.set_ylabel("True")
    ax.set_title("CNN baseline: validation confusion matrix (5000 samples)")
    for i in range(10):
        for j in range(10):
            if cm[i, j]:
                ax.text(j, i, str(cm[i, j]), ha="center", va="center", fontsize=6,
                        color="white" if cm[i, j] > cm.max() / 2 else "black")
    fig.colorbar(im, ax=ax, fraction=0.046)
    fig.tight_layout()
    fig.savefig(RESULTS_DIR / "cnn_validation_confusion_matrix.png", dpi=150)
    print("saved confusion matrix")

    # ---- most confused pairs (off-diagonal)
    pairs = []
    for i in range(10):
        for j in range(10):
            if i != j and cm[i, j] > 0:
                pairs.append({"true": CLASS_NAMES[i], "pred": CLASS_NAMES[j],
                              "count": int(cm[i, j]),
                              "rate_pct": round(100 * cm[i, j] / cm[i].sum(), 2)})
    pairs_df = pd.DataFrame(pairs).sort_values("count", ascending=False).head(12)
    pairs_df.to_csv(RESULTS_DIR / "cnn_validation_top_confusions.csv", index=False, encoding="utf-8-sig")
    print(pairs_df.to_string(index=False))


if __name__ == "__main__":
    main()
