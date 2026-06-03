# What changed and why

## The problem

Passwords and internal server addresses were written directly inside the source code.
Anyone who could read the code — or download the app package — could see them.

## What was moved out

| What | Where it lived | Where it lives now |
|---|---|---|
| MS Teams webhook URLs (with secret signatures) | `supporting.py` | `.env` |
| OTP secret key | `supporting.py` | `.env` |
| Login server address (LDAP) | `user_object.py` | `.env` |
| JIRA server address | `jira_session.py` | `.env` |
| SSO server address | `supporting.py` | `.env` |
| AI Chat server address | `8_AI_Chat_Interface.py` | `.env` |

## What was added

| File | Purpose |
|---|---|
| `Dockerfile` | Packages the app so it can run anywhere Docker is installed |
| `docker-compose.yml` | Describes how to build and run the container |
| `.env.example` | Template listing all required configuration values |

## Why this way

`.env` is a plain text file that lives only on the machine running the app.
It is listed in `.gitignore`, so it is never uploaded to the repository.

The source code now contains no addresses or secrets — it only reads them
from the environment at startup.

---

## Known limitations on Docker Linux

### Send Email page

The page uses Microsoft Outlook (win32com) to send emails, which is a Windows-only component and does not exist on Linux.

**Fix:** Replace with Python's built-in `smtplib` using the company's SMTP server.

### CyberArk credential retrieval

The code runs a PowerShell script to fetch passwords from CyberArk. PowerShell is not available on Linux.

**Fix:** CyberArk provides a REST API that can be called directly from Python without PowerShell.

### Database logging

The code points to a database file at a Windows network path (`\\vn-vwl5050\group2\...`). Linux containers cannot mount Windows network shares this way.

**Fix:** Store the database file inside the container, or migrate to a proper database server (PostgreSQL, MySQL) that both Linux and Windows can connect to.
