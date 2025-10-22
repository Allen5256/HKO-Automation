#!/usr/bin/env bash
set -euo pipefail
target="${1-}"
allure_dir="allure_results"
if [[ -z "${target}" ]]; then
  pytest --alluredir="${allure_dir}"
else
  echo "Target: ${target}"
  pytest -k "${target}" --alluredir="${allure_dir}"
fi
