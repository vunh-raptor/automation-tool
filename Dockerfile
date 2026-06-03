FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

ENV CHROME_BINARY=/usr/bin/chromium \
    CHROMEDRIVER_PATH=/usr/bin/chromedriver \
    CHROME_HEADLESS=true

ENV LDAP_URL=ldap://vn-ldaps.hcg.homecredit.net \
    LDAP_USER_OU="OU=Users,OU=VN,DC=hcg,DC=homecredit,DC=net" \
    LDAP_USER_GROUP_DN="CN=VN.SD.SD_AUTOMATION_HUB.USER,OU=Groups,OU=VN,DC=hcg,DC=homecredit,DC=net" \
    JIRA_URL=https://sd.homecredit.vn/rest/api/2/ \
    AI_CHAT_API_URL=http://sd-auto.homecredit.vn:1234/ask \
    SSO_URL=https://sso.homecredit.vn/opensso/identity/json/authenticate

ENV STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        chromium \
        chromium-driver \
        fonts-liberation \
        ca-certificates \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app
USER appuser

EXPOSE 8501

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://localhost:8501/_stcore/health || exit 1

CMD ["streamlit", "run", "main_site.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--browser.gatherUsageStats=false"]
