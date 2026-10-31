from pathlib import Path
import argparse
import csv
import time
import cv2
import torch
from ultralytics import YOLO

p = argparse.ArgumentParser()
p.add_argument("video", help="Path to a whole unseen MP4 game")
p.add_argument("--every", type=int, default=1,
               help="Process every Nth frame; 1 processes every frame")
p.add_argument("--conf", type=float, default=0.10)
args = p.parse_args()
if args.every < 1:
    raise SystemExit("--every must be at least 1")

weights = Path("runs/detect/disc5d/weights/best.pt")
if not weights.exists():
    raise SystemExit(f"Missing trained weights: {weights}")
model = YOLO(str(weights))
device = 0 if torch.cuda.is_available() else "cpu"

cap = cv2.VideoCapture(args.video)
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
if not cap.isOpened() or fps <= 0 or width <= 0 or height <= 0:
    raise SystemExit("Cannot read video, frame rate, or dimensions")

out = cv2.VideoWriter("review.mp4", cv2.VideoWriter_fourcc(*"mp4v"),
                      fps, (width, height))
if not out.isOpened():
    raise SystemExit("Could not create review.mp4")

processed = 0
index = 0
wall_start = time.perf_counter()
try:
    with open("detections.csv", "w", newline="", encoding="utf-8") as f:
        log = csv.writer(f)
        log.writerow(["frame", "video_seconds", "score", "x1", "y1",
                      "x2", "y2", "inference_ms"])
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if index % args.every == 0:
                start = time.perf_counter()
                result = model.predict(frame, imgsz=640, conf=args.conf,
                                       device=device, verbose=False)[0]
                ms = (time.perf_counter() - start) * 1000
                processed += 1
                for box in result.boxes:
                    x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
                    score = float(box.conf[0])
                    log.writerow([index, round(index / fps, 3),
                                  round(score, 4), x1, y1, x2, y2,
                                  round(ms, 1)])
                    cv2.rectangle(frame, (x1, y1), (x2, y2),
                                  (0, 255, 0), 2)
                    cv2.putText(frame, f"disc {score:.2f}", (x1, max(18, y1-5)),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6,
                                (0, 255, 0), 2)
            out.write(frame)
            index += 1
finally:
    cap.release()
    out.release()
elapsed = time.perf_counter() - wall_start
print(f"Read {index} frames; inferred on {processed}; "
      f"wall time {elapsed:.1f}s; processed frames/wall second "
      f"{processed / elapsed:.2f}")
print("Saved review.mp4 and detections.csv")