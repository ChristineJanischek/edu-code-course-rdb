#!/usr/bin/env bash
set -euo pipefail

root_dir="/workspaces/edu-code-course-rdb"

if [[ -x "$root_dir/.venv/bin/python" ]]; then
  python_bin="$root_dir/.venv/bin/python"
else
  python_bin="python3"
fi

exec "$python_bin" "$root_dir/scripts/sync_generated_html.py" "$@"