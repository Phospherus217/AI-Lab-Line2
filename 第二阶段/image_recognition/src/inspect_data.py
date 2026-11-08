from pathlib import Path
import numpy as np
import torch
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data"
CACHE = ROOT / "data" / "gui_cache.pt"
SIZE = 128
#CACHE:缓存

CLASSES = {"other" : 0, "login" : 1}

def decode_all():
    xs,ys=[],[]
    for cls,label in CLASSES.items():
        path = RAW / cls
        files = sorted(sorted(path.rglob("*.png"))+sorted(path.rglob("*.jpg")))
        print(f"类型:{cls} 数量:{len(files)}")

        buf = torch.empty(len(files),3,SIZE,SIZE,dtype=torch.uint8)
        for i,path in enumerate(files):
            img = Image.open(path).convert("RGB")
            img = img.resize((SIZE,SIZE),Image.LANCZOS)
            buf[i] = torch.from_numpy(np.array(img)).permute(2,0,1)
        xs.append(buf)
        ys.append(torch.full((len(files),),float(label)))
        # 只改零维
    return torch.cat(xs),torch.cat(ys)

def main():
    if CACHE.exists():
        print(f"已缓存{CACHE}")
        data = torch.load(CACHE)
        x, y = data["x"], data["y"]
    else:
        print("正在解码...")
        x, y = decode_all()
        torch.save({"x": x, "y": y}, CACHE)
        print("缓存成功!")
    print(f"x形状:{tuple(x.shape)} 类型:{x.dtype}")
    print(f"y形状:{tuple(y.shape)} 类型:{y.dtype}")
    print(f"登录页:{int((y == 1).sum())} 其他:{int((y == 0).sum())}")
    # y == 0     → tensor([ True, False,  True, False])
    # True == 1 但 True is 1 是错的
    # y == 1     → tensor([False,  True, False,  True])

if __name__ == "__main__":
    main()

