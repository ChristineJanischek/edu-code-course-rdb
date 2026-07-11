#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-milestone.sh --id TUI-005 [--output <datei>]

Beispiel:
  bash scripts/teacher-ui-milestone.sh --id TUI-005

Wirkung:
  - fuehrt den weiter-Trigger aus
  - erstellt Acceptance-Checks fuer die Meilensteinsteuerung
  - dokumentiert einen Regressionstestpfad als wiederholbare Checkliste
EOF
}

ID=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)
      ID="${2:-}"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="${2:-}"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "[milestone] ERROR: Unbekanntes Argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "[milestone] ERROR: --id ist erforderlich" >&2
  usage
  exit 1
fi

MILESTONE_DIR="generated/teacher-ui/milestones"
mkdir -p "$MILESTONE_DIR"

if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$MILESTONE_DIR/${ID}-milestone.md"
fi

bash scripts/weiter.sh >/dev/null

STATUS_FILE="generated/weiter-status.md"
if [[ ! -f "$STATUS_FILE" ]]; then
  echo "[milestone] ERROR: Weiter-Statusdatei fehlt: $STATUS_FILE" >&2
  exit 1
fi

extract_marker_value() {
  local label="$1"
  local value
  value="$(grep -E "^- ${label}: " "$STATUS_FILE" | head -n1 | sed -E 's/^.*: //')"
  if [[ -z "$value" ]]; then
    echo "no"
  else
    echo "$value"
  fi
}

m1="$(extract_marker_value 'M1 Baseline gesichert')"
m2="$(extract_marker_value 'M2 Hint-Modus \(API \+ UI\)')"
m3="$(extract_marker_value 'M3 Wissensanbindung \(Suche \+ Quellen\)')"
m4="$(extract_marker_value 'M4 Audit-Trail')"
m5="$(extract_marker_value 'M5 Lehrkraft-Features Fundament')"

status_line="$(grep -E '^## Naechster Milestone' -A2 "$STATUS_FILE" | tail -n1 | sed -E 's/^\s+//')"
timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

pass_fail() {
  local value="$1"
  if [[ "$value" == "yes" ]]; then
    echo "PASS"
  else
    echo "FAIL"
  fi
}

{
  echo "# ${ID} Milestone-Tracking Konsolidierung"
  echo
  echo "Erstellt am (UTC): $timestamp"
  echo
  echo "## Acceptance-Check weiter-Trigger"
  echo
  echo "- [$(pass_fail "$m1")] M1 Baseline gesichert = $m1"
  echo "- [$(pass_fail "$m2")] M2 Hint-Modus = $m2"
  echo "- [$(pass_fail "$m3")] M3 Wissensanbindung = $m3"
  echo "- [$(pass_fail "$m4")] M4 Audit-Trail = $m4"
  echo "- [$(pass_fail "$m5")] M5 Lehrkraft-Features Fundament = $m5"
  echo
  echo "Naechster Milestone laut weiter-Report: $status_line"
  echo
  echo "## Regressionstestpfad"
  echo
  echo "1. bash scripts/teacher-ui-intake.sh --id TUI-001"
  echo "2. bash scripts/teacher-ui-routing.sh --id TUI-002"
  echo "3. bash scripts/teacher-ui-todo.sh --id TUI-003"
  echo "4. bash scripts/teacher-ui-context.sh --id TUI-004"
  echo "5. bash scripts/teacher-ui-milestone.sh --id TUI-005"
  echo "6. bash scripts/sync-generated-html.sh --write"
  echo "7. bash scripts/validate-security.sh"
  echo "8. bash scripts/validate-architecture.sh"
  echo "9. bash scripts/validate-docs.sh"
  echo
  echo "## Konsolidierungsregeln"
  echo
  echo "- Der weiter-Trigger ist zentrale Instanz fuer den Entwicklungsstatus."
  echo "- TUI-Artefakte werden versionsiert unter generated/teacher-ui/ abgelegt."
  echo "- Jeder Lauf endet mit Pflicht-Gates und konsistenten HTML-Ableitungen."
} > "$OUTPUT_FILE"

echo "[milestone] OK: Milestone-Datei erzeugt: $OUTPUT_FILE"