from pathlib import Path

import numpy as np
from PIL import Image


def check_size(path: Path, expect: tuple[int, int]) -> dict:
    """检查图片尺寸。"""
    if not path.exists():
        return {"ok": False, "reason": "file_missing"}
    with Image.open(path) as im:
        size = im.size
    return {"ok": size == expect, "expect": expect, "actual": size}


def check_not_blank(path: Path, min_ratio: float = 0.01) -> dict:
    """检查不是空白图：非白像素占比 > min_ratio。"""
    with Image.open(path).convert("RGB") as im:
        arr = np.asarray(im).astype(int)
    non_white = (np.abs(arr - 255).sum(axis=2) > 20).mean()
    # bool() 很重要：numpy 的 bool 不能直接 json 序列化
    return {"ok": bool(non_white > min_ratio), "non_white_ratio": round(float(non_white), 4)}
