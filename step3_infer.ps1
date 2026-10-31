param(
    [Parameter(Mandatory=$true)]
    [string]$VideoPath
)

.\.venv\Scripts\Activate.ps1

Write-Host "=== Running Inference on: $VideoPath ===" -ForegroundColor Cyan
python infer.py $VideoPath --every 1 --conf 0.10

Write-Host "Done! Check your folder for review.mp4 and detections.csv." -ForegroundColor Green
