from config import ensure_directories, LABEL_DIR, VISUALIZATION_DIR
from evaluate import evaluate_one
from infer_ocr import load_ocr, run_ocr
from infer_yolo import load_yolo, run_yolo
from inspect_data import iter_images
from visualize import make_compare
from make_report import summarize, save_csv, save_markdown

def load_label(path):
    label_path = LABEL_DIR / (path.stem + ".txt")

    if not label_path.exists():
        return []

    items = []

    for line in label_path.read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) != 5:
            continue

        label = parts[0]

        x1, y1, x2, y2 = map(float, parts[1:])
        items.append({"box": [x1, y1, x2, y2],"label": label})

    return items

def main():
    """整体流程：读图 → 跑模型 → 存结果 → 画对比图 → 算指标 → 出报告。"""
    # 建好输出目录
    ensure_directories()
    # 加载两个模型（只加载一次，循环里复用）
    yolo_model = load_yolo()
    ocr_reader = load_ocr()
    rows = []
    for path, image, scale_width, scale_height in iter_images():
        # 1. 推理
        yolo_boxes = run_yolo(yolo_model, image)
        ocr_texts = run_ocr(ocr_reader, image)

        # 2. 读人工标注
        ground_truth_boxes = load_label(path)

        # 3. 算指标（只对 YOLO 算；OCR 的匹配方式另说）
        metrics = evaluate_one(yolo_boxes, ground_truth_boxes)

        # 合并成一行：文件名 + 各自数量 + 指标
        row = {
            "file": path.name,
            "yolo_count": len(yolo_boxes),
            "ocr_count": len(ocr_texts),
            **metrics,
        }
        rows.append(row)

        # 4. 画四联对比图
        make_compare(image, ground_truth_boxes, yolo_boxes, ocr_texts,
                     VISUALIZATION_DIR / f"{path.stem}_compare.png")

    save_csv(rows)
    save_markdown(rows)
    summarize(rows)

if __name__ == "__main__":
    main()