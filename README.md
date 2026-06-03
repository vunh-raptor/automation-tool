# This is a test edit

# What is Automation Hub?

Automation Hub is the centralized hub for all of Service Desk team's automation scripts. It is currently hosted in the Service Desk's GitLab.

The project is written in Python, utilizing Streamlit for front-end, and Selenium as the automation engine.

**GitLab**: https://git.homecredit.net/country/vn/service-desk/sd-automation-hub

# How to Install and Use

## Requirement

To run this scripting service, it is **required** to have two programs **pre-installed**:
- Python 3.12
- Git
- Chrome

All of the required softwares can be found in our Company Portal.

## Cloning & Pulling

To start with the scripting service, the user should clone the newest version of the **master** branch.

User with existing codebase can switch back to the master branch, fetch and pull the newest version.

More information on how to use git can be found [here](https://dev.azure.com/hc-vn/Services%20Management%20Team/_wiki/wikis/Services-Management-Team.wiki/5645/Git-Tutorial-for-Azure-DevOps).

## Setting Up the Required Library

This step is required only once per installation. Inside the sd-automation-hub folder, you will find the **setup.ps1** file. Open your preferred Terminal/PowerSshell and run `.\setup.ps1`


The installation will take a while. Please patiently wait until it is completed. Once it is done, you will find this message:

## Running the Script

To Run the script, run the `.run_script.ps1`. You can either run it from the Terminal or the ps1 file. Once it is done running, you will see the message below on the Terminal/Powershell.

Usually, it will automatically open a webpage with the mentioned Local URL. If it doesn't appear, you can always access the URL written on the Terminal/PowerShell

# Running with Docker

The repository ships with a `Dockerfile` that bundles Python 3.12, the Streamlit
front-end and a headless Chromium + chromedriver for the Selenium engine.

Build and run locally:

```bash
docker build -t sd-automation-hub:latest .
docker run --rm -p 8501:8501 --shm-size=1g sd-automation-hub:latest
```

Or with Docker Compose:

```bash
docker compose up --build
```

Then open http://localhost:8501.

The container is configured through environment variables (already set with sane
defaults in the image):

| Variable            | Default                  | Purpose                                  |
|---------------------|--------------------------|------------------------------------------|
| `CHROME_BINARY`     | `/usr/bin/chromium`      | Chrome/Chromium binary used by Selenium  |
| `CHROMEDRIVER_PATH` | `/usr/bin/chromedriver`  | chromedriver executable used by Selenium |
| `CHROME_HEADLESS`   | `true`                   | Run Chrome headless (no display)         |

> On Windows the defaults are unchanged: `CHROMEDRIVER_PATH` falls back to
> `chromedriver.exe` and Chrome runs with a visible window, so the existing
> `setup.ps1` / `run_script.ps1` workflow keeps working.
