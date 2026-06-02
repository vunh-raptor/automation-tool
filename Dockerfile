###############################################################################
# SD Automation Hub - Streamlit + Selenium container image
#
# Builds a self-contained image suitable for running on Kubernetes:
#   - Python 3.12 runtime
#   - Chromium + chromedriver for the Selenium automation engine
#   - Runs Streamlit as a non-root user on port 8501
###############################################################################
FROM python:3.12-slim AS base

# --- Runtime environment -----------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    # Selenium / page_object.py overrides so Chrome works inside the container
    CHROME_BINARY=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_HEADLESS=true \
    # Streamlit server defaults (also overridden on the CLI below)
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# --- System dependencies (Chromium browser + driver) -------------------------
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# --- Python dependencies (cached layer) --------------------------------------
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# --- Application code ---------------------------------------------------------
COPY . .

# --- Non-root user -----------------------------------------------------------
RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

# Streamlit's built-in health endpoint is used by the Kubernetes probes too.
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

# CLI flags take precedence over .streamlit/config.toml (which pins port 80),
# so we bind to the unprivileged 8501 port required for the non-root user.
CMD ["streamlit", "run", "main_site.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
