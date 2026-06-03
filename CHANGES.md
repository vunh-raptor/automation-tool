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
| `docker-compose.yml` | Describes how to run the container |
| `.env.example` | Template listing all required configuration values |
| `deploy.ps1` | One-click script to build and start the app |

## Why this way

`.env` is a plain text file that lives only on the machine running the app.
It is listed in `.gitignore`, so it is never uploaded to the repository.

The source code now contains no addresses or secrets — it only reads them
from the environment at startup.
