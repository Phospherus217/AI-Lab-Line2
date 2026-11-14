from pathlib import Path

# 集中存放常量和路径
ROOT = Path(__file__).resolve().parent.parent

IMAGE_DIR = ROOT / "data" / "images"
LABEL_DIR = ROOT / "data" / "labels"
OUTPUT_DIR = ROOT / "output"

YOLO_DIR = OUTPUT_DIR / "yolo"
OCR_DIR = OUTPUT_DIR / "ocr"
VISUALIZATION_DIR = OUTPUT_DIR / "visualization"

# 权重统一放在项目的 weight 目录，避免"从哪个目录运行就在哪下一份"
WEIGHT_DIR = ROOT / "weight"
# yolo模型
# YOLO_WEIGHT_PATH = WEIGHT_DIR / "yolov8n.pt"
YOLO_WEIGHT_PATH = WEIGHT_DIR / "best.pt"

# easyocr 的模型目录（检测器 craft + 识别器 zh_sim_g2 都放这里）
OCR_MODEL_DIR = WEIGHT_DIR / "easyocr"
# 统一缩放尺寸
IMAGE_SIZE = (2559, 1599)

# YOLO置信度
YOLO_CONFIDENCE_THRESHOLD = 0.25

# IoU 阈值：预测框和真实框的重叠比例
# 超过它才算"检对"。范围 0~1，0.5 是检测领域的传统标准
IOU_THRESHOLD = 0.5

def ensure_directories():
    for directory in (YOLO_DIR, OCR_DIR, VISUALIZATION_DIR):
        Path(directory).mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    ensure_directories()

