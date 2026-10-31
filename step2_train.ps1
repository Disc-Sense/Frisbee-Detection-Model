.\.venv\Scripts\Activate.ps1

Write-Host "=== Training YOLO Model ===" -ForegroundColor Cyan
python train.py train --epochs 35 --batch 8

Write-Host "=== Evaluating on Test Split ===" -ForegroundColor Cyan
python train.py test

Write-Host "Training and evaluation complete!" -ForegroundColor Green
