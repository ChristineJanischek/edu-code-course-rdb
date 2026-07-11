#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-context.sh --id TUI-004 [--routing <datei>] [--todo <datei>] [--output <datei>]

Beispiele:
  bash scripts/teacher-ui-context.sh --id TUI-004
  bash scripts/teacher-ui-context.sh --id TUI-004 --routing generated/teacher-ui/routing/TUI-002-routing.md --todo generated/teacher-ui/todos/TUI-003-todo.md

Wirkung:
  - aggregiert Routing- und To-do-Ergebnisse
  - erstellt Kontext-KI-Zuordnung fuer bestehende Course-Arbeitsfenster
  - liefert Smoke-Test-Checkliste fuer UI-Integration
EOF
}

ID=""
ROUTING_FILE="generated/teacher-ui/routing/TUI-002-routing.md"
TODO_FILE="generated/teacher-ui/todos/TUI-003-todo.md"
OUTPUT_FILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --id)
      ID="${2:-}"
      shift 2
      ;;
    --routing)
      ROUTING_FILE="${2:-}"
      shift 2
      ;;
    --todo)
      TODO_FILE="${2:-}"
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
      echo "[context] ERROR: Unbekanntes Argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "[context] ERROR: --id ist erforderlich" >&2
  usage
  exit 1
fi

if [[ ! -f "$ROUTING_FILE" ]]; then
  echo "[context] ERROR: Routing-Datei nicht gefunden: $ROUTING_FILE" >&2
  exit 1
fi

if [[ ! -f "$TODO_FILE" ]]; then
  echo "[context] ERROR: To-do-Datei nicht gefunden: $TODO_FILE" >&2
  exit 1
fi

CONTEXT_DIR="generated/teacher-ui/context"
mkdir -p "$CONTEXT_DIR"

if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$CONTEXT_DIR/${ID}-context.md"
fi

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

REQ_COUNT="$(grep -c '^- Text: ' "$ROUTING_FILE" || true)"
TASK_COUNT="$(grep -c '^### Task ' "$TODO_FILE" || true)"

{
  echo "# ${ID} Kontextbezogene KI im Arbeitsfenster"
  echo
  echo "Erstellt am (UTC): $timestamp"
  echo
  echo "Quellen:"
  echo
  echo "- Routing: $ROUTING_FILE"
  echo "- To-do: $TODO_FILE"
  echo
  echo "## Zusammenfassung"
  echo
  echo "- Erkannte Anforderungen: $REQ_COUNT"
  echo "- Generierte To-do-Tasks: $TASK_COUNT"
  echo "- Ziel: KI-Hinweise direkt in bestehende Arbeitsfenster integrieren, ohne neue Hauptreiter einzufuehren."
  echo
  echo "## Kontext-KI-Zuordnung pro Arbeitsfenster"
  echo
  echo "### Kurseditor > Planung"
  echo
  echo "- KI-Aktion: Lernziel-Check und Themenreihenfolge-Hinweis"
  echo "- Trigger: Bei Modulwechsel oder leerem Planungsfeld"
  echo "- Ausgabe: Kurzvorschlag mit 1-3 konkreten naechsten Schritten"
  echo
  echo "### Aufgabeneditor > Erstellung"
  echo
  echo "- KI-Aktion: Aufgabendifferenzierung und Schwierigkeitsabgleich"
  echo "- Trigger: Beim Speichern oder Check der Aufgabenformulierung"
  echo "- Ausgabe: Hinweise zu Klarheit, Taxonomiestufe und moeglichen Hilfestellungen"
  echo
  echo "### Abgaben > Rueckmeldung"
  echo
  echo "- KI-Aktion: Feedback-Bausteine und Fehlercluster-Hinweise"
  echo "- Trigger: Nach Bewertungseingabe oder bei haeufigen Fehlern"
  echo "- Ausgabe: knappe Feedback-Optionen mit Lernfokus"
  echo
  echo "## Usability-Regeln"
  echo
  echo "1. Keine neue Hauptnavigation fuer einzelne KI-Funktionen."
  echo "2. KI-Ausgaben bleiben kompakt und kontextnah (maximal 5 Punkte)."
  echo "3. Jede KI-Aktion hat klaren Trigger und sichtbare Rueckmeldung."
  echo "4. Lehrkraft kann Hinweise uebernehmen, anpassen oder verwerfen."
  echo
  echo "## UI-Smoke-Test-Checkliste"
  echo
  echo "- [ ] Kurseditor zeigt Kontext-KI-Hinweis bei relevanten Planungsaktionen."
  echo "- [ ] Aufgabeneditor zeigt Differenzierungs-Hinweise ohne Layoutbruch."
  echo "- [ ] Abgabenbereich zeigt Feedback-Hilfen kontextbezogen."
  echo "- [ ] Bestehende Navigation bleibt unveraendert und uebersichtlich."
  echo "- [ ] Fehlerfall wird nutzerfreundlich angezeigt (ohne interne Details)."
  echo
  echo "## Testvorschlaege"
  echo
  echo "- Integrationstest: Pro Arbeitsfenster wird genau eine passende KI-Aktion angeboten."
  echo "- UI-Test: Kein neuer Hauptreiter entsteht durch TUI-004."
  echo "- Robustheitstest: Bei fehlenden Daten bleibt die Seite bedienbar und zeigt fallback-Hinweis."
} > "$OUTPUT_FILE"

echo "[context] OK: Kontext-Datei erzeugt: $OUTPUT_FILE"
