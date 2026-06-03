if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
    Write-Host ""
    Write-Host "File .env vua duoc tao tu .env.example"
    Write-Host "Vui long mo file .env va dien 3 gia tri bat buoc:"
    Write-Host "  - REACTIVATE_WEBHOOK_URL"
    Write-Host "  - ERROR_WEBHOOK_URL"
    Write-Host "  - OTP_SECRET"
    Write-Host ""
    Write-Host "Sau do chay lai: .\deploy.ps1"
    exit 1
}

docker compose up --build -d

Write-Host ""
Write-Host "App dang chay tai: http://localhost:8501"
