#!/usr/bin/env bash
# Stage 1 (verify): mirror the production `verify` job.
# Run it INSIDE your WSL2 distro (Ubuntu), not PowerShell.
#
#   ./stage1-verify.sh           # default: run in the python:3.12 container (matches CI exactly)
#   LOCAL=1 ./stage1-verify.sh   # instead use your WSL2 host's own python3
#
# Installs deps, checks Streamlit, and byte-compiles the entrypoint.
set -euo pipefail

# repo root = two levels up from simulation/scripts
cd "$(dirname "$0")/../.."

if [ "${LOCAL:-0}" = "1" ]; then
  python3 -m pip install --no-cache-dir -r requirements.txt
  streamlit --version
  python3 -m py_compile main_site.py
else
  # exact same base image as .gitlab-ci.yml's `verify` job
  docker run --rm -v "$PWD":/app -w /app python:3.12 bash -lc '
    pip install --no-cache-dir -r requirements.txt &&
    streamlit --version &&
    python -m py_compile main_site.py'
fi

echo "verify: OK"
