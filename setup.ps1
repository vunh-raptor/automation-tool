<#
.SYNOPSIS
This script sets up a Python virtual environment and installs the necessary dependencies.

.DESCRIPTION
The script performs the following steps:
1. Creates a Python virtual environment in a directory named "venv".
2. Activates the virtual environment.
3. Installs the Python packages specified in the "requirements.txt" file.

.EXAMPLE
.\setup.ps1

#>
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r .\requirements.txt