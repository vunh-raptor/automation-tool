#!/bin/bash
set -e

if [ ! -f .env ]; then
    cp .env.example .env
    echo ""
    echo "File .env vừa được tạo từ .env.example"
    echo "Vui lòng mở file .env và điền 3 giá trị bắt buộc:"
    echo "  - REACTIVATE_WEBHOOK_URL"
    echo "  - ERROR_WEBHOOK_URL"
    echo "  - OTP_SECRET"
    echo ""
    echo "Sau đó chạy lại: ./deploy.sh"
    exit 1
fi

docker compose up --build -d

echo ""
echo "App đang chạy tại: http://localhost:8501"
