from PIL import Image, ImageDraw, ImageFont

from config import VISUALIZATION_DIR

COLOR_GROUND_TRUTH = (0, 200, 0)       # 绿色：人工标注
COLOR_YOLO = (230, 40, 40)             # 红色：YOLO
COLOR_OCR = (30, 120, 240)             # 蓝色：OCR

# 字体只在导入时加载一次，不要每画一个框都加载
FONT_PATH = "C:/Windows/Fonts/msyh.ttc"      # 微软雅黑，支持中英文
FONT_SIZE = 16

def draw_boxes(image, items , color ,thickness = 3):
    """
    在一张图上画框，返回画好的 PIL 图。
    items 里每项要有 "box" 字段；
    如果有 "label" 或 "text"，会写在框的上方。
    """
    drawn = Image.fromarray(image.copy())
    drawer = ImageDraw.Draw(drawn)
    # 加载中文字体：PIL 默认字体没有汉字，会画成方框
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    for item in items:
        x1,y1,x2,y2 = item["box"]
        drawer.rectangle([x1,y1,x2,y2], outline=color, width=thickness)
        caption = item.get("label") or item.get("text") or ""

        if caption:
            drawer.text((x1 + 2, max(0, y1 - 12)), str(caption), fill=(0, 0, 0), font=font)
    return drawn

def make_compare(original, ground_truth_items, yolo_items, ocr_items, output_path):
    """
    生成"原图 / 人工 / YOLO / OCR"四联图。
    为什么要四联：一张图就能看出漏检和误检，比纯文字有说服力。
    """
    panels = [
        Image.fromarray(original),  # 原图
        draw_boxes(original, ground_truth_items, COLOR_GROUND_TRUTH),  # 人工标注
        draw_boxes(original, yolo_items, COLOR_YOLO),  # YOLO
        draw_boxes(original, ocr_items, COLOR_OCR),  # OCR
    ]
    width, height = panels[0].size
    canvas = Image.new("RGB", (width * 4, height), (30, 30, 30))
    for index, panel in enumerate(panels):
        canvas.paste(panel, (index * width, 0))

    canvas.save(output_path)

if __name__ == "__main__":
    import json
    from config import IMAGE_DIR, VISUALIZATION_DIR, YOLO_DIR, OCR_DIR
    from inspect_data import iter_images
    items = json.loads((YOLO_DIR / "deepseek&&claude.json").read_text(encoding="utf-8"))
    for _, image ,_ ,_ in iter_images(IMAGE_DIR):
        drawn = draw_boxes(image, items["boxes"], COLOR_YOLO)
        drawn.save(VISUALIZATION_DIR / "test.png")
        break


