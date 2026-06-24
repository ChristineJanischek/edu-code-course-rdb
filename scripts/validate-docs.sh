#!/usr/bin/env bash
set -euo pipefail

fail=0

note_fail() {
  echo "[docs] FAIL: $1"
  fail=1
}

echo "[docs] Starte Dokumentationsvalidierung..."

if ! bash scripts/validate-content-catalog.sh; then
  echo "[docs] FAIL: normalisierte Content-DB oder abgeleitete Artefakte sind nicht synchron"
  echo "[docs] HINT: bash scripts/generate-content-catalog.sh"
  exit 1
fi

if ! bash scripts/sync-generated-html.sh --check; then
  echo "[docs] FAIL: HTML-Exporte aus Markdown oder Stoffverlaufsplan sind nicht synchron"
  echo "[docs] HINT: bash scripts/sync-generated-html.sh"
  exit 1
fi

if ! python3 scripts/optimize_docs.py --check; then
  echo "[docs] FAIL: Dokumentation ist nicht wohlgeformt oder strukturell inkonsistent"
  echo "[docs] HINT: bash scripts/optimize-docs.sh"
  exit 1
fi

if ! bash scripts/validate-central-entrypoints.sh; then
  echo "[docs] FAIL: zentrale Einstiegspunkt-Regel fuer README-Dateien verletzt"
  exit 1
fi

required_files=(
  "docs/handbuch/INDEX.md"
  "docs/handbuch/PFLICHTENHEFT.md"
  "docs/handbuch/ARCHITEKTUR.md"
  "docs/handbuch/marschplaene/HAUPTMARSCHPLAN.md"
  "docs/handbuch/prozesse/review-prozess.md"
  "docs/handbuch/prozesse/qualitaets-gates-automatisierung.md"
  "docs/handbuch/anleitungen/java-live-test.md"
)

for file in "${required_files[@]}"; do
  [[ -f "$file" ]] || note_fail "Fehlende Pflichtdokumentation: $file"
done

template_file="docs/handbuch/templates/ROUTINE-TEMPLATE.md"

if ! grep -nE "^### Metadata$" "$template_file" >/dev/null 2>&1; then
  note_fail "Template unvollstaendig, Abschnitt fehlt: Metadata"
fi

if ! grep -nE "^### .*Ziel" "$template_file" >/dev/null 2>&1; then
  note_fail "Template unvollstaendig, Abschnitt fehlt: Ziel"
fi

if ! grep -nE "^### .*Schritte" "$template_file" >/dev/null 2>&1; then
  note_fail "Template unvollstaendig, Abschnitt fehlt: Schritte"
fi

if ! grep -nE "^### .*Erfolgskriterien" "$template_file" >/dev/null 2>&1; then
  note_fail "Template unvollstaendig, Abschnitt fehlt: Erfolgskriterien"
fi

if ! grep -nE "^### .*Changelog" "$template_file" >/dev/null 2>&1; then
  note_fail "Template unvollstaendig, Abschnitt fehlt: Changelog"
fi

changed_files=""
if git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
  changed_files="$(git diff --name-only HEAD~1 HEAD || true)"
else
  changed_files="$(git ls-files)"
fi

if echo "$changed_files" | grep -E "^(src/|services/|webapp/)" >/dev/null 2>&1; then
  if ! echo "$changed_files" | grep -E "^docs/handbuch/" >/dev/null 2>&1; then
    note_fail "Codeaenderung ohne Handbuch-Aktualisierung erkannt."
  fi
fi

if [[ $fail -ne 0 ]]; then
  echo "[docs] Dokumentationsvalidierung fehlgeschlagen"
  exit 1
fi

if ! bash scripts/validate-ka-separate-context.sh; then
  echo "[docs] FAIL: Klassenarbeits-Kontexttrennung fehlgeschlagen"
  exit 1
fi

if ! bash scripts/validate-ka-language-quality.sh; then
  echo "[docs] FAIL: Klassenarbeits-Sprachqualitaet fehlgeschlagen"
  exit 1
fi

echo "[docs] Dokumentationsvalidierung erfolgreich"
