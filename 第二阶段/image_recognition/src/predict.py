from pathlib import Path
import numpy as np
import torch
from PIL import Image
from model import ImagenetModel

ROOT = Path(__file__).resolve().parent.parent
SIZE = 128
MEAN = [0.485, 0.456, 0.406]
STD = [0.229, 0.224, 0.225]
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

@torch.no_grad()
def predict(image_path):
    model = ImagenetModel().to(DEVICE)
    model.load_state_dict(torch.load(ROOT / "output" / "best.pt"))
    model.eval()
    image = Image.open(image_path)
    image = image.convert("RGB")
    image = image.resize((SIZE, SIZE), Image.LANCZOS)
    x = (torch.from_numpy(np.array(image)).float()/255.0).permute(2, 0, 1)
    for i in range(3):
        x[i] = (x[i] - MEAN[i]) / STD[i]
    x = x.unsqueeze(0).to(DEVICE)
    pred = torch.sigmoid(model(x))
    return pred

def mian():
    print(f"请输入图片路径!")
    image_path = Path(input())
    if not image_path.exists():
        print(f"图片不存在,用默认图!")
    path = image_path if image_path.exists() else ROOT / "data" /"predict" / ("bilibili.png")
    pred = predict(path)
    label = "登录页" if pred > 0.5 else "其他"
    print(f"文件 :{path}")
    print(f"P(登录页) = {pred.item():.3f}")
    print(f"结果 :{label}")

if __name__ == "__main__":
    mian()