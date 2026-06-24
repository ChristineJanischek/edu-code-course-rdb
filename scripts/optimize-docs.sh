#!/usr/bin/env bash
set -euo pipefail

echo "[docs-opt] Starte automatische Dokumentationsoptimierung..."
bash scripts/generate-content-catalog.sh
bash scripts/sync-generated-html.sh --write
python3 scripts/optimize_docs.py --write
echo "[docs-opt] Verifiziere Struktur nach Optimierung..."
bash scripts/validate-content-catalog.sh
bash scripts/sync-generated-html.sh --check
python3 scripts/optimize_docs.py --check
echo "[docs-opt] Dokumentation ist wohlgeformt und konsistent"
