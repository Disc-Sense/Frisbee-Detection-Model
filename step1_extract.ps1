.\.venv\Scripts\Activate.ps1

Write-Host "=== Extracting frames from videos ===" -ForegroundColor Cyan
python extract.py train
python extract.py val
python extract.py test

Write-Host "Extraction complete! STOP HERE and label your frames in data\labels\ before training." -ForegroundColor Yellow
