#!/usr/bin/env bash
# -----------------------------------------------------------------------
# generate-ka-struktogramme.sh
# Generiert SVG-Struktogramme für Klassenarbeiten aus XML-Definitionen.
# Verwendung: bash scripts/generate-ka-struktogramme.sh [ka-name]
# Beispiel:   bash scripts/generate-ka-struktogramme.sh ka02
# Ohne Argument: alle bekannten KA-Sätze generieren.
# -----------------------------------------------------------------------
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CONVERTER="$SCRIPT_DIR/struktogramme/converter/struktogramm_xml_renderer.py"
OUT_DIR="$REPO_ROOT/generated/klassenarbeiten/svg"

mkdir -p "$OUT_DIR"

generate_set() {
    local xml_dir="$1"
    echo "[struktogramme] Generiere aus: $xml_dir"
    python3 - <<PYEOF
import sys
sys.path.insert(0, "$SCRIPT_DIR/struktogramme/converter")
from struktogramm_xml_renderer import BWStruktogrammRenderer
from pathlib import Path

renderer = BWStruktogrammRenderer()
xml_dir = Path("$xml_dir")
out_dir = Path("$OUT_DIR")

for xml_file in sorted(xml_dir.glob("*.xml")):
    svg = renderer.xml_to_svg(str(xml_file))
    svg_file = out_dir / (xml_file.stem + ".svg")
    svg_file.write_text(svg, encoding="utf-8")
    print(f"  OK: {svg_file.relative_to(Path('$REPO_ROOT'))}")
PYEOF
}

KA_ARG="${1:-all}"

if [[ "$KA_ARG" == "all" || "$KA_ARG" == "ka02" ]]; then
    generate_set "$SCRIPT_DIR/struktogramme/xml_definitions/ka02"
fi

echo "[struktogramme] Fertig. SVGs in: generated/klassenarbeiten/svg/"
