#!/usr/bin/env bash
set -euo pipefail

echo "[ka-separate-context] Starte Validierung fuer getrennten SQL-Kontext..."

fail=0

note_fail() {
  echo "[ka-separate-context] FAIL: $1"
  fail=1
}

check_file_exists() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    note_fail "Fehlendes Artefakt: $file"
  fi
}

check_mwb_container() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    return
  fi

  if ! unzip -tqq "$file" >/dev/null 2>&1; then
    note_fail "Kein gueltiger .mwb-Container (ZIP erwartet): $file"
    return
  fi

  if ! unzip -l "$file" | awk '{print $4}' | grep -qx "document.mwb.xml"; then
    note_fail "Kein natives Workbench-Modell (document.mwb.xml fehlt): $file"
    return
  fi

  local doc_xml
  if ! doc_xml="$(unzip -p "$file" document.mwb.xml 2>/dev/null)"; then
    note_fail "document.mwb.xml kann nicht gelesen werden: $file"
    return
  fi

  if ! printf '%s' "$doc_xml" | grep -q '<data[[:space:]][^>]*grt_format='; then
    note_fail "Kein echtes Workbench-GRT-XML (data grt_format fehlt): $file"
    return
  fi

  if ! printf '%s' "$doc_xml" | grep -q 'workbench\.physical\.Model'; then
    note_fail "Kein echtes Workbench-Modellobjekt (workbench.physical.Model fehlt): $file"
  fi
}

check_max_entity_types() {
  local sql_file="$1"
  local max_entities=6
  local entity_count
  entity_count=$(grep -cE '^\s*CREATE\s+TABLE\s+' "$sql_file" || true)

  if [[ "$entity_count" -gt "$max_entities" ]]; then
    note_fail "$sql_file: zu viele Entitaetstypen ($entity_count > $max_entities)"
  fi
}

check_md_html_pairs() {
  local dir="generated/klassenarbeiten"

  # Every KA markdown (aufg/lsg) must have a matching HTML export.
  for md in "$dir"/KA*_*.md; do
    [[ -e "$md" ]] || continue
    case "$md" in
      *_aufg.md|*_lsg.md)
        local html="${md%.md}.html"
        if [[ ! -f "$html" ]]; then
          note_fail "Fehlender HTML-Export fuer Markdown: $html"
        fi
        ;;
    esac
  done

  # Every KA HTML must have a matching markdown source.
  for html in "$dir"/KA*_*.html; do
    [[ -e "$html" ]] || continue
    local md="${html%.html}.md"
    if [[ ! -f "$md" ]]; then
      note_fail "Verwaiste HTML-Datei ohne Markdown-Quelle: $html"
    fi
  done
}

check_md_html_pairs

# KF-ROUTINE-010: KA-Loesungsdokumente folgen *_lsg.md Konvention.
# Artefakt-Pruefung: {systemname}_{year}.mwb, {systemname}_struktur_{year}.sql, {systemname}_{year}.png
for md in generated/klassenarbeiten/*_lsg.md; do
  [[ -e "$md" ]] || continue

  base_name="${md##*/}"
  dir="generated/klassenarbeiten"

  # Lese SQL-/Modellartefakte aus YAML-Frontmatter
  sql_dump_name=$(grep -oP '^\s*sql_db_dump:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')
  sql_data_name=$(grep -oP '^\s*sql_db_daten:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')
  sql_eerm_name=$(grep -oP '^\s*sql_db_eerm:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')
  sql_png_name=$(grep -oP '^\s*sql_db_eerm_grafik:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')
  eerm_lehrkraft=$(grep -oP '^\s*modellierung_eerm_lehrkraft:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')

  [[ -n "$sql_dump_name" ]] && sql_dump="$dir/$sql_dump_name" || sql_dump=""
  [[ -n "$sql_data_name" ]] && sql_data="$dir/$sql_data_name" || sql_data=""
  [[ -n "$sql_eerm_name" ]] && sql_model="$dir/$sql_eerm_name" || sql_model=""
  [[ -n "$sql_png_name" ]] && sql_png="$dir/$sql_png_name" || sql_png=""
  [[ -n "$eerm_lehrkraft" ]] && model_part_b="$dir/$eerm_lehrkraft" || model_part_b=""

  if [[ -n "$sql_dump_name" ]] && [[ "$sql_dump_name" != *_struktur_*.sql ]]; then
    note_fail "$md: sql_db_dump muss auf *_struktur_*.sql zeigen"
  fi
  if [[ -n "$sql_data_name" ]] && [[ "$sql_data_name" != *_daten_*.sql ]]; then
    note_fail "$md: sql_db_daten muss auf *_daten_*.sql zeigen"
  fi

  [[ -n "$sql_dump" ]] && check_file_exists "$sql_dump"
  [[ -n "$sql_data" ]] && check_file_exists "$sql_data"
  [[ -n "$sql_dump" ]] && [[ -f "$sql_dump" ]] && check_max_entity_types "$sql_dump"
  [[ -n "$model_part_b" ]] && check_file_exists "$model_part_b"
  [[ -n "$sql_model" ]] && check_file_exists "$sql_model"
  [[ -n "$model_part_b" ]] && [[ -f "$model_part_b" ]] && check_mwb_container "$model_part_b"
  [[ -n "$sql_model" ]] && [[ -f "$sql_model" ]] && check_mwb_container "$sql_model"

  if ! grep -qi "separater sql-kontext" "$md"; then
    note_fail "$md: Hinweis auf separaten SQL-Kontext fehlt"
  fi

  if ! grep -qi "anderen kontext" "$md"; then
    note_fail "$md: didaktische Trennung Teil B/Teil C nicht klar benannt"
  fi

  if ! grep -qi "3nf" "$md"; then
    note_fail "$md: 3NF-Anforderung fuer SQL-Kontext fehlt"
  fi

  if [[ -n "$sql_png" ]] && [[ -f "$sql_png" ]]; then
    echo "[ka-separate-context] INFO: Workbench-Grafik gefunden: $sql_png"
  elif [[ -n "$sql_png" ]]; then
    echo "[ka-separate-context] INFO: Keine Workbench-Grafik gefunden, versuche Generator: $sql_png"
    python3 scripts/plugins/eerm_grafik_generator/generate_eerm_png.py --input-dir "$dir" || true
    if [[ -f "$sql_png" ]]; then
      echo "[ka-separate-context] INFO: Grafik per Generator erstellt: $sql_png"
    else
      echo "[ka-separate-context] WARN: Keine Workbench-Grafik gefunden (optional): $sql_png"
    fi
  fi

done

if [[ $fail -ne 0 ]]; then
  echo "[ka-separate-context] Validierung fehlgeschlagen"
  exit 1
fi

echo "[ka-separate-context] Validierung erfolgreich"
