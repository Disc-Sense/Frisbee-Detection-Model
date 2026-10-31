from ultralytics import YOLO

model = YOLO("runs/detect/disc5d/weights/best.pt")
model.predict(
    source="data/images/test",
    imgsz=640,
    conf=0.10,
    save=True,
    project="runs/review",
    name="test_images",
    exist_ok=True,
)
print("Open runs/review/test_images to inspect the predicted boxes.")
