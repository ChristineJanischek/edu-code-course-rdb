#!/usr/bin/env bash
set -euo pipefail

root_dir="/workspaces/edu-code-course-rdb"
cd "$root_dir"

marker="<!-- CENTRAL_ENTRYPOINT -->"

central_files=(
  "README.md"
  "generated/README.md"
  "docs/handbuch/README.md"
)

fail=0

note_fail() {
  echo "[entrypoints] FAIL: $1"
  fail=1
}

contains_path() {
  local needle="$1"
  shift
  for item in "$@"; do
    if [[ "$item" == "$needle" ]]; then
      return 0
    fi
  done
  return 1
}

echo "[entrypoints] Pruefe zentrale Einstiegspunkte..."

for file in "${central_files[@]}"; do
  if [[ ! -f "$file" ]]; then
    note_fail "Pflichtdatei fehlt: $file"
    continue
  fi

  if ! grep -F "$marker" "$file" >/dev/null 2>&1; then
    note_fail "Marker fehlt in zentralem Einstiegspunkt: $file"
  fi
done

mapfile -t readme_files < <(git ls-files '**/README.md' 'README.md' | sort)

for file in "${readme_files[@]}"; do
  if contains_path "$file" "${central_files[@]}"; then
    continue
  fi

  if grep -F "$marker" "$file" >/dev/null 2>&1; then
    note_fail "Unerlaubter zentraler Marker in Nicht-Zentraldatei: $file"
  fi

done

# Schutz vor alternativen "Start hier"-Formulierungen in nicht-zentralen READMEs.
for file in "${readme_files[@]}"; do
  if contains_path "$file" "${central_files[@]}"; then
    continue
  fi

  if grep -Ei '(^|[^a-z])(start hier|du bist hier|primaerer startpunkt|primärer startpunkt|zentrale dokumentation|zentraler einstiegspunkt)($|[^a-z])' "$file" >/dev/null 2>&1; then
    note_fail "Nicht-zentrale README beansprucht Startpunkt-Rolle: $file"
  fi

done

if [[ $fail -ne 0 ]]; then
  echo "[entrypoints] FEHLER: Einstiegspunkt-Regel verletzt"
  echo "[entrypoints] Erlaubte zentrale Einstiegspunkte:"
  for file in "${central_files[@]}"; do
    echo "[entrypoints]   - $file"
  done
  exit 1
fi

echo "[entrypoints] OK"
