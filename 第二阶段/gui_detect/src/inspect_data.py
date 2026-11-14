from pathlib import Path

import numpy as np
from PIL import Image

from config import IMAGE_SIZE,IMAGE_DIR

def list_images(folder=IMAGE_DIR):
    """
    列出所有截图路径，按文件名排序。
    排序是为了每次跑的图顺序固定，结果可复现。
    """
    images_extensions = ['.jpg', '.jpeg', '.png']
    files = [f for f in Path(folder).iterdir() if f.suffix.lower() in images_extensions]
    files.sort()
    return files

def load_images(path,target_size = IMAGE_SIZE):
    """
    读一张图，缩放到固定尺寸，并返回缩放比例。
    """
    image = Image.open(path).convert('RGB')
    original_width, original_height = image.size
    image = image.resize(target_size, Image.LANCZOS)
    array = np.array(image)
    scale_width = target_size[0] / original_width
    scale_height = target_size[1] / original_height
    return array, scale_width, scale_height

def iter_images(folder=IMAGE_DIR, target_size = IMAGE_SIZE):
    """
    逐张产出 (路径, 图像数组, scale_x, scale_y)。
    用生成器：以后几百张图也不会一次性占满内存。
    """
    if Path(folder).exists():
        for path in list_images(folder):
            array, scale_width, scale_height = load_images(path,target_size)
            yield path, array, scale_width, scale_height
        # yield 生成器,产出一个之后暂停
    else:
        print(f"文件不存在!")


if __name__ == "__main__":
    # 测试
    if not list_images():
        print(f"目录是空的，请先把截图放进：{IMAGE_DIR}")
        raise SystemExit(0)
    for path, array, scale_width, scale_height in iter_images():
        print(path.name, array.shape, round(scale_width, 3), round(scale_height, 3))
        # round( , 3)保留三位小数
        break
    print(f"导入完成!")