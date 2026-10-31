from pathlib import Path
import argparse
import torch
from ultralytics import YOLO

p = argparse.ArgumentParser()
p.add_argument("action", choices=("train", "test"))
p.add_argument("--epochs", type=int, default=35)
p.add_argument("--batch", type=int, default=8)
args = p.parse_args()

root = Path("data").resolve().as_posix()
yaml_text = (
    f"path: '{root}'\n"
    "train: images/train\n"
    "val: images/val\n"
    "test: images/test\n"
    "names:\n  0: disc\n"
)
Path("data.yaml").write_text(yaml_text, encoding="utf-8")
device = 0 if torch.cuda.is_available() else "cpu"
print("Using device:", device)

if args.action == "train":
    model = YOLO("yolo11n.pt")  # Downloads pretrained weights on first use.
    model.train(data="data.yaml", imgsz=640, epochs=args.epochs,
                batch=args.batch, workers=0, device=device,
                project=str(Path("runs/detect").resolve()), name="disc5d", exist_ok=True)
else:
    weights = Path("runs/detect/disc5d/weights/best.pt")
    if not weights.exists():
        raise SystemExit(f"Missing trained weights: {weights}")
    model = YOLO(str(weights))
    model.val(data="data.yaml", split="test", imgsz=640,
              device=device, project=str(Path("runs/test").resolve()), name="heldout",
              exist_ok=True)