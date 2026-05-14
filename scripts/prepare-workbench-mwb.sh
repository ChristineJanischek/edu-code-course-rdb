#!/usr/bin/env bash
set -euo pipefail

python3 scripts/generate_mwb_from_sql.py "$@"
