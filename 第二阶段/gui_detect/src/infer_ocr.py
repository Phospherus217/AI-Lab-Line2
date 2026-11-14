import json
import easyocr

from config import OCR_DIR, OCR_MODEL_DIR
from inspect_data import iter_images

def load_ocr(languages=("ch_sim", "en")):
    r"""
    加载 OCR 模型。
    ch_sim = 简体中文，en = 英文。

    model_storage_directory：把模型目录固定到项目的 weight/easyocr，
    这样不会跑到用户目录 C:\Users\xxx\.EasyOCR\model 去下第二份。
    """
    return easyocr.Reader(
        list(languages),
        gpu=True,
        model_storage_directory=str(OCR_MODEL_DIR),
        download_enabled=True,
    )

def run_ocr(reader, image):
    """对一张图做 OCR，返回统一格式的文字块。
        不是矩形框,要我们自己转
        raw_results = [
        ([[12.3, 108.5], [88.1, 108.2], [88.4, 132.7], [12.6, 133.0]], "登录", 0.973),
        ([[...], [...], [...], [...]], "发送验证码", 0.912),
        ...]
        返回：
            [{"box": [x1,y1,x2,y2], "score": 0.93, "text": "登录"}, ...]

        easyocr 原始输出是四点坐标，要转成左上右下的矩形。
    """
    raw_results = reader.readtext(image)
    texts = []
    for points, text, score in raw_results:
        # points 形如 [[x,y], [x,y], [x,y], [x,y]]
        all_x = [point[0] for point in points]
        all_y = [point[1] for point in points]
        x1, x2 = float(min(all_x)), float(max(all_x))
        y1, y2 = float(min(all_y)), float(max(all_y))

        if len(text.strip()) == 0:
            continue

        texts.append({
            "box": [round(x1,1),round(y1,1),round(x2,1),round(y2,1)],
            "score": round(float(score), 3),
            "text": text,
        })
    return texts

def save_result(path, texts, output_dir=OCR_DIR):
    """存 json，和 YOLO 的格式保持一致。"""
    data = {"file": path.name,"texts": texts}
    output_path = output_dir / (path.stem + ".json")
    output_path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

def run_all(reader):
    for path, image, scale_width, scale_height in iter_images():
        texts = run_ocr(reader, image)
        save_result(path, texts)
        print(f"{path.name}: 读到 {len(texts)} 段文字")

if __name__ == "__main__":
    run_all(load_ocr())
