from pathlib import Path

errors = []
for split in ("train", "val", "test"):
    images = sorted(
        p for p in Path("data/images", split).iterdir()
        if p.suffix.lower() in (".jpg", ".jpeg", ".png")
    )
    positive = negative = 0
    for image in images:
        label = Path("data/labels", split, image.stem + ".txt")
        if not label.exists():
            errors.append(f"Missing label: {label}")
            continue
        lines = [line.strip() for line in label.read_text(encoding="utf-8-sig").splitlines()
                 if line.strip()]
        if not lines:
            negative += 1
        else:
            positive += 1
        for line in lines:
            parts = line.split()
            try:
                if len(parts) != 5 or parts[0] != "0":
                    raise ValueError("Expected: 0 x_center y_center width height")
                x, y, w, h = map(float, parts[1:])
                if not (0 <= x <= 1 and 0 <= y <= 1 and
                        0 < w <= 1 and 0 < h <= 1 and
                        x - w/2 >= -0.001 and x + w/2 <= 1.001 and
                        y - h/2 >= -0.001 and y + h/2 <= 1.001):
                    raise ValueError("Box extends outside the image")
            except ValueError as exc:
                errors.append(f"{label}: {line!r} — {exc}")
    if not images:
        errors.append(f"No images found in data/images/{split}")
    print(f"{split}: {len(images)} images; {positive} with labels; "
          f"{negative} empty/no-disc labels")

if errors:
    print("\nPROBLEMS:")
    print("\n".join(errors[:30]))
    raise SystemExit(f"Fix {len(errors)} problem(s) before training.")
print("\nBasic label checks passed.")
