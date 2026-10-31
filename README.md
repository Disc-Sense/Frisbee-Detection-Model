# Frisbee Detection Model

This repository contains a small YOLO-based pipeline for detecting discs (frisbees) in game video.

- `extract.py` and `step1_extract.ps1` implement frame extraction.
- `train.py` and `step2_train.ps1` implement training and test evaluation.
- `infer.py` implements inference on an unseen video, including annotated
  video output and CSV detection logging.

## Directory layout

```text
.
├── extract.py             # Extracts frames from game videos
├── train.py               # Trains and evaluates the YOLO model
├── infer.py               # Applies trained weights to a video
├── step1_extract.ps1      # PowerShell frame-extraction step
├── step2_train.ps1        # PowerShell training/evaluation step
├── step3_infer.ps1        # PowerShell inference step
├── games/
│   ├── train/             # Training videos (*.mp4)
│   ├── val/               # Validation videos (*.mp4)
│   └── test/              # Test videos (*.mp4)
└── data/
    ├── images/{train,val,test}/
    └── labels/{train,val,test}/
```

## Setup

Use Python 3 and run all commands from the repository root. The scripts expect
the virtual environment to be at `.venv`.

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install opencv-python torch ultralytics
```

If PowerShell blocks activation scripts, allow scripts for the current user
and then activate the environment:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
.\.venv\Scripts\Activate.ps1
```

## PowerShell workflow

### Check to see that each image has a .txt file

```powershell
python check_dataset.py
```

### Train model

Only if check passes

```powershell
python train.py train --epochs 35 --batch 8
```

### Test model

```powershell
python train.py test
```

### Visualize testing

```powershell
python predict_images.py
```

<!-- The first two scripts have no parameters; the third requires a video path.

### 1. Extract frames

Place `.mp4` files in `games/train`, `games/val`, and `games/test`, then run:

```powershell
& .\step1_extract.ps1
```

### 2. Label, train, and evaluate

Before training, label the extracted images. Labels use the YOLO detection
format: one line per disc containing
`class_id center_x center_y width height`, with coordinates normalized to
`0..1`. This project has one class, `disc`, so the class ID is `0`. Empty
label files represent frames with no visible disc.

Open `data/labels/` and add your YOLO `.txt` labels (`class_id center_x center_y width height`). Class ID for `disc` is `0`.

After labeling, run:

```powershell
& .\step2_train.ps1
```


### 3. Run inference

Test the trained model on a new, unseen game video:

```powershell
& .\step3_infer.ps1 -VideoPath .\games\test\example.mp4
```

This generates two outputs in the root folder:

- `review.mp4`: the input video with detected discs outlined and scored; and
- `detections.csv`: frame number, video time, confidence, bounding-box coordinates, and inference time.

This step requires the trained file
`runs/detect/disc5d/weights/best.pt`. The input video is not modified; outputs
are written to the repository root. -->

## Git Ignore

To keep the repository clean and prevent tracking large generated files, make sure your `.gitignore` includes:

```text
.venv/
games/
data/
data.yaml
runs/
review.mp4
detections.csv