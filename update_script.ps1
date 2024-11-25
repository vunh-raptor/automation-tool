<#
.SYNOPSIS
This script activates a virtual environment and updates the local git repository.

.DESCRIPTION
The script performs the following steps:
1. Activates a Python virtual environment located at .\venv\Scripts\.
2. Fetches the latest changes from the remote git repository.
3. Merges the fetched changes into the current branch.
4. Installs the required Python packages listed in the requirements.txt file.

#>

.\venv\Scripts\Activate.ps1
git fetch
git pull
pip install -r requirements.txt
