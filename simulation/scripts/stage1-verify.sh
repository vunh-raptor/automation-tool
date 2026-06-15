#!/usr/bin/env bash
# Stage 1 (verify): mirror the production `verify` job locally.
# Installs deps, checks Streamlit, and byte-compiles the entrypoint.
set -euo pipefail

# repo root = two levels up from simulation/scripts
cd "$(dirname "$0")/../.."

python3 -m pip install --no-cache-dir -r requirements.txt
streamlit --version
python3 -m py_compile main_site.py

echo "verify: OK"
