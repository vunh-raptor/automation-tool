###############################################################################
# SD Automation Hub - Streamlit + Selenium container image
#
#   - Python 3.12 runtime
#   - Chromium + chromedriver for the Selenium automation engine
#   - Runs Streamlit as a non-root user on port 8501
#
# Secrets (REACTIVATE_WEBHOOK_URL, ERROR_WEBHOOK_URL, OTP_SECRET) are NOT
# set here — they must be injected at runtime via docker-compose env_file
# or -e flags to avoid baking secrets into the image layer.
###############################################################################
FROM python:3.12-slim AS base

# --- Python / pip behaviour --------------------------------------------------
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

# --- Chrome / Selenium (page_object.py reads these) --------------------------
ENV CHROME_BINARY=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_HEADLESS=true

# --- Internal service URL defaults (override at runtime if needed) -----------
ENV LDAP_URL=ldap://vn-ldaps.hcg.homecredit.net \
    LDAP_USER_OU="OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net" \
    LDAP_USER_GROUP_DN="CN=VN.SD.SD_AUTOMATION_HUB.USER,OU=Groups,OU=VN,DC=hcg,DC=homecredit,DC=net" \
    JIRA_URL=https://sd.homecredit.vn/rest/api/2/ \
    AI_CHAT_API_URL=http://sd-auto.homecredit.vn:1234/ask \
    SSO_URL=https://sso.homecredit.vn/opensso/identity/json/authenticate

# --- Streamlit server defaults -----------------------------------------------
ENV STREAMLIT_SERVER_PORT=8501 \
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

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

# CLI flags take precedence over .streamlit/config.toml (which pins port 80),
# so we bind to the unprivileged 8501 port required for the non-root user.
CMD ["streamlit", "run", "main_site.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
