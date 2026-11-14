import json

from ultralytics import YOLO

from config import YOLO_DIR, YOLO_CONFIDENCE_THRESHOLD, YOLO_WEIGHT_PATH
from inspect_data import iter_images

def load_yolo(weight_name=str(YOLO_WEIGHT_PATH)):
    """
    加载预训练 YOLO 模型。
    """
    return YOLO(weight_name)

def run_yolo(model, image, confidence_threshold=YOLO_CONFIDENCE_THRESHOLD):
    results = model([image], conf=confidence_threshold, verbose=False)
    result = results[0]

    boxes = []
    for index in range(len(result.boxes)):
        # cls: tensor([], device='cuda:0')
        # conf: tensor([], device='cuda:0')
        # data: tensor([], device='cuda:0', size=(0, 6))
        # id: None
        # is_track: False
        # orig_shape: (720, 1280)
        # shape: torch.Size([0, 6])
        # xywh: tensor([], device='cuda:0', size=(0, 4))
        # xywhn: tensor([], device='cuda:0', size=(0, 4))
        # xyxy: tensor([], device='cuda:0', size=(0, 4))
        # xyxyn: tensor([], device='cuda:0', size=(0, 4))
        box = result.boxes[index]
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        score = float(box.conf[0])
        class_id = int(box.cls[0])
        label = result.names[class_id]
        boxes.append({
            "box": [round(x1, 1), round(y1, 1), round(x2, 1), round(y2, 1)],
            "score": round(score, 3),
            "label": label
        })
    return boxes

def save_result(path, boxes, output_dir = YOLO_DIR):
    """存 json，和 YOLO 的格式保持一致。"""
    data = {"file" : path.name, "boxes" : boxes}
    output_path = output_dir / (path.stem + ".json")
    output_path.write_text(json.dumps(data,ensure_ascii=False,indent=1), encoding="utf-8")

def run_all(model):
    """对所有截图跑一遍 OCR，逐张存 json。"""
    for path, image, scale_width, scale_height in iter_images():
        boxes = run_yolo(model, image)
        save_result(path, boxes)
        print(f"{path.name}: 检出 {len(boxes)} 个框")

if __name__ == "__main__":
    run_all(load_yolo())


# for path, image, scale_width, scale_height in iter_images():
#     print(run_yolo(load_yolo(), image))
#     break
