#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-routing.sh --id TUI-002 [--input <datei>] [--output <datei>]

Beispiele:
  bash scripts/teacher-ui-routing.sh --id TUI-002
  bash scripts/teacher-ui-routing.sh --id TUI-002 --input generated/teacher-ui/intake/TUI-001-structured.md

Wirkung:
  - liest strukturierte Anforderungen
  - ordnet Prozesse, UI-Hauptbereich und Darstellungsform zu
  - erzeugt priorisierte Routing-Ausgabe mit Testvorschlaegen
EOF
}

ID=""
INPUT_FILE=""
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)
      ID="${2:-}"
      shift 2
      ;;
    --input)
      INPUT_FILE="${2:-}"
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
      echo "[routing] ERROR: Unbekanntes Argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "[routing] ERROR: --id ist erforderlich" >&2
  usage
  exit 1
fi

ROUTING_DIR="generated/teacher-ui/routing"
mkdir -p "$ROUTING_DIR"

if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$ROUTING_DIR/${ID}-routing.md"
fi

if [[ -z "$INPUT_FILE" ]]; then
  INPUT_FILE="generated/teacher-ui/intake/TUI-001-structured.md"
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "[routing] ERROR: Input-Datei nicht gefunden: $INPUT_FILE" >&2
  exit 1
fi

REQ_TMP="$(mktemp)"
awk '/^## Erkannte Einzelanforderungen/{flag=1;next}/^## /{flag=0}flag' "$INPUT_FILE" \
  | sed -E 's/^[0-9]+\.\s+//' \
  | sed -E 's/^ +//; s/ +$//' \
  | awk 'length($0) > 0' > "$REQ_TMP"

if [[ ! -s "$REQ_TMP" ]]; then
  echo "[routing] ERROR: Keine Anforderungen im Abschnitt 'Erkannte Einzelanforderungen' gefunden" >&2
  rm -f "$REQ_TMP"
  exit 1
fi

map_process() {
  local text="$1"
  local lower
  lower="$(echo "$text" | tr '[:upper:]' '[:lower:]')"

  if echo "$lower" | grep -Eq 'bewert|feedback|abgabe'; then
    echo "Feedback geben"
  elif echo "$lower" | grep -Eq 'aufgabe|veroeffentlich|differenz'; then
    echo "Aufgabe erstellen"
  elif echo "$lower" | grep -Eq 'kurs|unterricht|lernziel|material'; then
    echo "Unterricht planen"
  else
    echo "Kurs verwalten"
  fi
}

map_ui_area() {
  local process="$1"
  case "$process" in
    "Unterricht planen")
      echo "Kurseditor > Planung"
      ;;
    "Aufgabe erstellen")
      echo "Aufgabeneditor > Erstellung"
      ;;
    "Feedback geben")
      echo "Abgaben > Rueckmeldung"
      ;;
    *)
      echo "Kursverwaltung > Uebersicht"
      ;;
  esac
}

map_view_mode() {
  local text="$1"
  local lower
  lower="$(echo "$text" | tr '[:upper:]' '[:lower:]')"

  if echo "$lower" | grep -Eq 'transkrib|sprache|eingabe'; then
    echo "Assistent"
  elif echo "$lower" | grep -Eq 'liste|to-do|todo|uebersicht'; then
    echo "Seitenleiste"
  else
    echo "Kontextdialog"
  fi
}

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
  echo "# ${ID} Prozess- und UI-Zuordnung"
  echo
  echo "Erstellt am (UTC): $timestamp"
  echo
  echo "Quelle: $INPUT_FILE"
  echo
  echo "## Routing-Ergebnis"
  echo

  i=1
  while IFS= read -r req; do
    process="$(map_process "$req")"
    ui_area="$(map_ui_area "$process")"
    view_mode="$(map_view_mode "$req")"

    echo "### Anforderung $i"
    echo
    echo "- Text: $req"
    echo "- Prozess: $process"
    echo "- UI-Hauptbereich: $ui_area"
    echo "- Darstellungsform: $view_mode"
    echo "- Prioritaet: Hoch"
    echo
    i=$((i+1))
  done < "$REQ_TMP"

  echo "## Routing-Qualitaetskriterien"
  echo
  echo "1. Jede Anforderung enthaelt Prozesszuordnung."
  echo "2. Jede Anforderung enthaelt UI-Hauptbereich und Darstellungsform."
  echo "3. Zuordnung folgt Prozess statt Technikmodul."
  echo "4. Haeufige Funktionen landen in schnell erreichbaren Bereichen."
  echo
  echo "## Testvorschlaege"
  echo
  echo "- Mapping-Test: Prozesszuordnung fuer typische Lehreraufgaben."
  echo "- UI-Zuordnungstest: Hauptbereich bleibt stabil bei Synonymen."
  echo "- Robustheitstest: Eingaben ohne Prozesswoerter fallen auf Default-Kursverwaltung."
} > "$OUTPUT_FILE"

rm -f "$REQ_TMP"

echo "[routing] OK: Routing-Datei erzeugt: $OUTPUT_FILE"
