# Dùng Python 3.12 làm nền tảng, bản slim để image nhỏ gọn hơn
FROM python:3.12-slim AS base

# Cấu hình Python và pip
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# Đường dẫn tới Chrome bên trong container, chạy ở chế độ không cần màn hình
ENV CHROME_BINARY=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_HEADLESS=true

# Cấu hình Streamlit: chạy ở port 8501, lắng nghe mọi kết nối, tắt telemetry
ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Cài Chrome và các gói hệ thống cần thiết
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

# Thư mục làm việc bên trong container
WORKDIR /app

# Cài Python dependencies trước — bước này được cache lại,
# chỉ chạy lại khi requirements.txt thay đổi
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ code vào container
COPY . .

# Tạo user thường để chạy app, không dùng root
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

# Khai báo port app sẽ lắng nghe
EXPOSE 8501

# Kiểm tra app còn sống không, cứ 30 giây check một lần
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

# Lệnh khởi động app
CMD ["streamlit", "run", "main_site.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
