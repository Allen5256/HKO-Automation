#!/usr/bin/env bash
set -euo pipefail
python -m venv .venv
. ./.venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
echo "Done. Activate: source ./.venv/bin/activate"
