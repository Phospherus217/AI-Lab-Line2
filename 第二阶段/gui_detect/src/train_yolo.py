from pathlib import Path
from ultralytics import YOLO
from config import YOLO_WEIGHT_PATH

ROOT = Path(__file__).resolve().parent.parent
DATA_CONFIG = ROOT / "dataset" / "gui" / "data.yaml"
TRAIN_OUTPUT_DIR = ROOT / "train_output"

def main():
    if not DATA_CONFIG.exists():
        print(f"找不到数据配置：{DATA_CONFIG}")
        print("请先运行 python src/make_dataset.py")
        return

    # 从预训练权重开始（不是从零初始化）
    model = YOLO(str(YOLO_WEIGHT_PATH))

    model.train(
        data=str(DATA_CONFIG),  # 数据配置（唯一必填项）
        epochs=50,  # 训练轮数
        imgsz=640,  # 输入尺寸
        batch=8,  # 8GB 显存用 8
        lr0=0.001,  # 微调用小学习率
        freeze=10,  # 冻结骨干前 10 层，小数据更稳
        patience=10,  # 10 轮没提升就早停
        workers=2,  # Windows 上别用默认的 8
        project=str(TRAIN_OUTPUT_DIR),  # 结果放哪
        name="gui_finetune",  # 这次实验的名字
        exist_ok=False,  # False：不覆盖，自动变成 gui_finetune2
    )

    metrics = model.val()
    print("\n=== 验证集指标 ===")
    print(f"mAP@0.5      : {metrics.box.map50:.4f}")
    print(f"mAP@0.5:0.95 : {metrics.box.map:.4f}")
    print(f"\n新权重在：{TRAIN_OUTPUT_DIR}\\gui_finetune\\weights\\best.pt")

if __name__ == "__main__":
    main()