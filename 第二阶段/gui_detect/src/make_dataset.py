from pathlib import Path
import yaml
from PIL import Image
from config import IMAGE_DIR, LABEL_DIR

DATASET_DIR = Path(__file__).resolve().parent.parent / "dataset" / "gui"
TRAIN_IMAGES = DATASET_DIR / "images" / "train"
VAL_IMAGES = DATASET_DIR / "images" / "val"
TRAIN_LABELS = DATASET_DIR / "labels" / "train"
VAL_LABELS = DATASET_DIR / "labels" / "val"

# 统一尺寸：和标注时用的尺寸一致，这样标签不用换算
IMAGE_SIZE = (2559, 1599)

# 类别名 → 编号（顺序决定 data.yaml 里的 names）
CLASS_TO_ID = {"button": 0, "input": 1, "icon": 2, "link": 3, "other": 4}
# "按钮": 0, "输入框": 1, "图标": 2, "链接": 3, "其他": 4

# 训练/验证切分比例
TRAIN_RATIO = 0.8

def make_directories():
    for directories in (TRAIN_IMAGES, VAL_IMAGES, TRAIN_LABELS, VAL_LABELS):
        Path(directories).mkdir(parents=True, exist_ok=True)

def convert_label(labels_path,out_path):
    for label_path in labels_path:
        out = []
        lines = label_path.read_text(encoding="utf-8").splitlines()
        for line in lines:
            parts = line.split()
            if len(parts) != 5:
                parts.clear()
                continue
            name = change_name(parts[0])
            x1, y1, x2, y2 = map(float,parts[1:])
            cx = ((x1 + x2) / 2) / IMAGE_SIZE[0]
            cy = ((y1 + y2) / 2) / IMAGE_SIZE[1]
            w = (x2 - x1) / IMAGE_SIZE[0]
            h = (y2 - y1) / IMAGE_SIZE[1]
            out.append(f"{name} {cx} {cy} {w} {h}")
        (out_path / (label_path.stem + label_path.suffix)).write_text("\n".join(out), encoding="utf-8")

def split_images(pairs):
    train_labels = []
    val_labels = []

    split_index = max(1, int(len(pairs) * TRAIN_RATIO))

    for index, (image_path, label_path) in enumerate(pairs):
        if index < split_index:
            train_labels.append(label_path)
            image = Image.open(image_path).convert("RGB")
            image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
            image.save(TRAIN_IMAGES / (image_path.stem + image_path.suffix))
        else:
            val_labels.append(label_path)
            image = Image.open(image_path).convert("RGB")
            image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
            image.save(VAL_IMAGES / (image_path.stem + image_path.suffix))
    print("Train images: ", len(train_labels))
    print("val images: ", len(val_labels))
    return split_index, train_labels, val_labels

def change_name(name):
    if name in CLASS_TO_ID.keys():
        return CLASS_TO_ID[name]
    else:
        return CLASS_TO_ID["other"]
def write_yaml():
    config = {
        "path": str(DATASET_DIR).replace("\\", "/"),  # yaml 里用正斜杠更稳
        "train": "images/train",
        "val": "images/val",
        "names": {v: k for k, v in CLASS_TO_ID.items()},
    }
    yaml_path = DATASET_DIR / "data.yaml"
    yaml_path.write_text(
        yaml.safe_dump(config, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    return yaml_path


def main():
    make_directories()
    pairs = []
    images_extensions = ['.jpg', '.jpeg', '.png']
    for image_path in sorted(path for suffix in images_extensions for path in Path(IMAGE_DIR).rglob("*" + suffix)):
        label_path = LABEL_DIR / (image_path.stem + ".txt")
        if label_path.exists():
            pairs.append((image_path, label_path))

    if not pairs:
        print("没有找到带标注的图片!")
        return

    print(f"共 {len(pairs)} 张带标注的图片")

    split_index, train_labels, val_labels = split_images(pairs)
    convert_label(train_labels, TRAIN_LABELS)
    convert_label(val_labels, VAL_LABELS)

    yaml_path = write_yaml()

    print(f"\n导入完成：训练 {split_index} 张，验证 {len(pairs) - split_index} 张")
    print(f"数据配置：{yaml_path}")

if __name__ == "__main__":
    main()