#!/usr/bin/env bash
set -euo pipefail

echo "[mwb-native] Starte Validierung nativer Workbench-Dateien..."

fail=0
dir="generated/klassenarbeiten"

note_fail() {
  echo "[mwb-native] FAIL: $1"
  fail=1
}

if [[ ! -d "$dir" ]]; then
  note_fail "Verzeichnis fehlt: $dir"
  echo "[mwb-native] Validierung fehlgeschlagen"
  exit 1
fi

check_native_mwb() {
  local file="$1"

  if [[ ! -f "$file" ]]; then
    note_fail "Fehlende .mwb-Datei: $file"
    return
  fi

  if ! unzip -tqq "$file" >/dev/null 2>&1; then
    note_fail "Kein gueltiger ZIP-Container: $file"
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

  # Echte Workbench-Modelle enthalten GRT-XML mit data/grt_format und workbench.physical.Model.
  if ! printf '%s' "$doc_xml" | grep -q '<data[[:space:]][^>]*grt_format='; then
    note_fail "Kein echtes Workbench-GRT-XML (data grt_format fehlt): $file"
    return
  fi

  if ! printf '%s' "$doc_xml" | grep -q 'workbench\.physical\.Model'; then
    note_fail "Kein echtes Workbench-Modellobjekt (workbench.physical.Model fehlt): $file"
    return
  fi

  if printf '%s' "$doc_xml" | grep -q 'generated_mwb_from_sql\.py\|generated_by="scripts/generate_mwb_from_sql.py"'; then
    note_fail "Pseudo-MWB erkannt (nicht mit MySQL Workbench gespeichert): $file"
  fi
}

declare -a referenced_mwb=()

for md in "$dir"/*_lsg.md; do
  [[ -e "$md" ]] || continue

  model_part_b=$(grep -oP '^\s*modellierung_eerm_lehrkraft:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')
  model_sql_part_c=$(grep -oP '^\s*sql_db_eerm:\s*["\x27]?\K[^"\x27\n]+' "$md" | head -1 | sed 's/^\s*//; s/\s*$//')

  if [[ -n "$model_part_b" ]]; then
    referenced_mwb+=("$dir/$model_part_b")
  else
    note_fail "$md: Frontmatter-Feld modellierung_eerm_lehrkraft fehlt"
  fi

  if [[ -n "$model_sql_part_c" ]]; then
    referenced_mwb+=("$dir/$model_sql_part_c")
  else
    note_fail "$md: Frontmatter-Feld sql_db_eerm fehlt"
  fi
done

if [[ ${#referenced_mwb[@]} -eq 0 ]]; then
  note_fail "Keine referenzierten .mwb-Dateien in *_lsg.md gefunden"
fi

if [[ ${#referenced_mwb[@]} -gt 0 ]]; then
  mapfile -t unique_mwb < <(printf '%s\n' "${referenced_mwb[@]}" | sort -u)
  for mwb in "${unique_mwb[@]}"; do
    check_native_mwb "$mwb"
  done

  echo "[mwb-native] Gepruefte .mwb-Dateien: ${#unique_mwb[@]}"
fi

if [[ $fail -ne 0 ]]; then
  echo "[mwb-native] Validierung fehlgeschlagen"
  exit 1
fi

echo "[mwb-native] Validierung erfolgreich"
