#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-todo.sh --id TUI-003 [--input <datei>] [--output <datei>]

Beispiele:
  bash scripts/teacher-ui-todo.sh --id TUI-003
  bash scripts/teacher-ui-todo.sh --id TUI-003 --input generated/teacher-ui/routing/TUI-002-routing.md

Wirkung:
  - liest Routing-Ergebnisse
  - erzeugt priorisierte To-do-Eintraege je Funktionswunsch
  - ergaenzt Akzeptanzkriterien und technische Teilaufgaben
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
      echo "[todo] ERROR: Unbekanntes Argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "[todo] ERROR: --id ist erforderlich" >&2
  usage
  exit 1
fi

if [[ -z "$INPUT_FILE" ]]; then
  INPUT_FILE="generated/teacher-ui/routing/TUI-002-routing.md"
fi

if [[ ! -f "$INPUT_FILE" ]]; then
  echo "[todo] ERROR: Input-Datei nicht gefunden: $INPUT_FILE" >&2
  exit 1
fi

TODO_DIR="generated/teacher-ui/todos"
mkdir -p "$TODO_DIR"

if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$TODO_DIR/${ID}-todo.md"
fi

REQ_TMP="$(mktemp)"
awk '/^- Text: /{sub(/^- Text: /,""); print}' "$INPUT_FILE" > "$REQ_TMP"

if [[ ! -s "$REQ_TMP" ]]; then
  echo "[todo] ERROR: Keine Text-Eintraege im Routing-Dokument gefunden" >&2
  rm -f "$REQ_TMP"
  exit 1
fi

priority_for() {
  local text="$1"
  local lower
  lower="$(echo "$text" | tr '[:upper:]' '[:lower:]')"

  if echo "$lower" | grep -Eq 'to-do|todo|akzeptanzkriter|technisch'; then
    echo "Kritisch"
  elif echo "$lower" | grep -Eq 'transkrib|sprache|zerlegt'; then
    echo "Hoch"
  else
    echo "Mittel"
  fi
}

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
  echo "# ${ID} Automatische To-do-Generierung"
  echo
  echo "Erstellt am (UTC): $timestamp"
  echo
  echo "Quelle: $INPUT_FILE"
  echo
  echo "## Priorisierte To-do-Eintraege"
  echo

  i=1
  while IFS= read -r req; do
    prio="$(priority_for "$req")"
    echo "### Task $i"
    echo
    echo "- Ausgangsanforderung: $req"
    echo "- Prioritaet: $prio"
    echo "- Status: Offen"
    echo "- Fachlicher Schritt: Anforderung praezisieren und in UI-Flow einordnen"
    echo "- Technischer Schritt: Controller/Service-Schnittstelle planen"
    echo "- Testschritt: Routing + Ergebnisdarstellung pruefen"
    echo
    i=$((i+1))
  done < "$REQ_TMP"

  echo "## Akzeptanzkriterien"
  echo
  echo "1. Jede Routing-Anforderung erzeugt genau einen To-do-Eintrag."
  echo "2. Jeder To-do-Eintrag enthaelt Prioritaet, fachlichen Schritt, technischen Schritt und Testschritt."
  echo "3. Kritische Anforderungen werden vorrangig vor Mittel priorisiert."
  echo "4. Ausgabe ist als markdownbasiertes Artefakt versionierbar."
  echo
  echo "## Technische Teilaufgaben"
  echo
  echo "- Parser fuer Routing-Textfelder"
  echo "- Priorisierungsregel nach Schluesselbegriffen"
  echo "- Ausgabe-Renderer fuer standardisierte Taskstruktur"
  echo
  echo "## Testvorschlaege"
  echo
  echo "- Vollstaendigkeitstest: Anzahl Tasks entspricht Anzahl Routing-Anforderungen."
  echo "- Priorisierungstest: To-do-bezogene Anforderungen werden als Kritisch markiert."
  echo "- Robustheitstest: Fehler bei leerem/ungueltigem Input wird sauber ausgegeben."
} > "$OUTPUT_FILE"

rm -f "$REQ_TMP"

echo "[todo] OK: To-do-Datei erzeugt: $OUTPUT_FILE"
