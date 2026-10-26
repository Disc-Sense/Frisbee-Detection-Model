from pathlib import Path
import argparse
import cv2

p = argparse.ArgumentParser()
p.add_argument("split", choices=("train", "val", "test"))
p.add_argument("--interval", type=float, default=1.0,
               help="Seconds between extracted frames")
args = p.parse_args()
if args.interval <= 0:
    raise SystemExit("--interval must be positive")

videos = sorted(Path("games", args.split).glob("*.mp4"))
if not videos:
    raise SystemExit(f"No MP4 files found in games/{args.split}")

for video in videos:
    cap = cv2.VideoCapture(str(video))
    fps = cap.get(cv2.CAP_PROP_FPS)
    if not cap.isOpened() or fps <= 0:
        raise SystemExit(f"Cannot open or read frame rate: {video}")
    step = max(1, round(fps * args.interval))
    index = saved = 0
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        if index % step == 0:
            # Include split and video name to avoid filenames colliding.
            stem = f"{args.split}_{video.stem}_{index:08d}"
            image = Path("data/images", args.split, stem + ".jpg")
            label = Path("data/labels", args.split, stem + ".txt")
            if not cv2.imwrite(str(image), frame):
                raise SystemExit(f"Could not save {image}")
            label.touch(exist_ok=True)  # Empty = no visible disc.
            saved += 1
        index += 1
    cap.release()
    print(f"{video}: {saved} images at approximately {args.interval}s intervals")
