#!/usr/bin/env bash
set -euo pipefail

# Automatismus fuer 3 Klassenarbeitsversionen je Terminlogik:
# VERSION1 (Haupttermin), VERSION2 (Nachtermin), VERSION3 (Muster/Uebung)

root_dir="/workspaces/edu-code-course-rdb"
ka_dir="$root_dir/generated/klassenarbeiten"
convert_script="$root_dir/scripts/convert_ka_markdown.py"
assets_script="$root_dir/scripts/generate-ka-eerm-assets.sh"
struktogramm_script="$root_dir/scripts/generate-ka-struktogramme.sh"

if [[ -x "$root_dir/.venv/bin/python" ]]; then
  py="$root_dir/.venv/bin/python"
else
  py="python3"
fi

prefix="${1:-KA02_BG12_2025_2026}"

echo "[ka-varianten] Prefix: $prefix"

declare -a expected
for v in 1 2 3; do
  expected+=("$ka_dir/${prefix}_VERSION${v}_aufg.md")
  expected+=("$ka_dir/${prefix}_VERSION${v}_lsg.md")
done

missing=0
for file in "${expected[@]}"; do
  if [[ ! -f "$file" ]]; then
    echo "[ka-varianten] FAIL: fehlende Datei: $file"
    missing=1
  fi
done

if [[ "$missing" -ne 0 ]]; then
  echo "[ka-varianten] Abbruch: Versionen unvollstaendig"
  exit 1
fi

# Distinkte Kontexte pruefen (pro VERSION-Loesungsdatei)
declare -A seen_model

declare -A seen_sql
for v in 1 2 3; do
  lsg="$ka_dir/${prefix}_VERSION${v}_lsg.md"
  model=$(grep -oP '^\s*modellierung_eerm_lehrkraft:\s*["\x27]?\K[^"\x27\n]+' "$lsg" | head -1 | sed 's/^\s*//; s/\s*$//')
  sqls=$(grep -oP '^\s*sql_db_dump:\s*["\x27]?\K[^"\x27\n]+' "$lsg" | head -1 | sed 's/^\s*//; s/\s*$//')

  if [[ -z "$model" || -z "$sqls" ]]; then
    echo "[ka-varianten] FAIL: Artefaktfelder fehlen in $lsg"
    exit 1
  fi

  if [[ -n "${seen_model[$model]:-}" ]]; then
    echo "[ka-varianten] FAIL: Modellkontext doppelt: $model (Version ${seen_model[$model]} und VERSION${v})"
    exit 1
  fi
  if [[ -n "${seen_sql[$sqls]:-}" ]]; then
    echo "[ka-varianten] FAIL: SQL-Kontext doppelt: $sqls (Version ${seen_sql[$sqls]} und VERSION${v})"
    exit 1
  fi

  seen_model[$model]="$v"
  seen_sql[$sqls]="$v"
done

echo "[ka-varianten] Kontextvariationen OK (3 unterschiedliche Versionen)"

ka_set=$(echo "$prefix" | sed -E 's/^KA([0-9]+).*/ka\1/' | tr '[:upper:]' '[:lower:]')

echo "[ka-varianten] Struktogramm-SVG-Artefakte erzeugen ($ka_set)..."
bash "$struktogramm_script" "$ka_set"

echo "[ka-varianten] EERM-PNG-Artefakte erzeugen..."
bash "$assets_script" --force

echo "[ka-varianten] HTML-Exporte erzeugen (inkl. Grafik-Einbettung und Tabellenlayout)..."
"$py" "$convert_script"

echo "[ka-varianten] Fertig"
