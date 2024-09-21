<#
.SYNOPSIS
This script activates the virtual environment and runs the Streamlit application.

.DESCRIPTION
The script first activates the virtual environment located in the venv/Scripts directory.
Then, it runs the Streamlit application defined in the main_site.py file.

.EXAMPLE
.\run_script.ps1

#>
.\venv\Scripts\Activate.ps1 
streamlit run main_site.py