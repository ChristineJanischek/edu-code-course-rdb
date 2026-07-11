#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-intake.sh --id TUI-001 [--input <datei>] [--output <datei>]

Beispiele:
  bash scripts/teacher-ui-intake.sh --id TUI-001
  bash scripts/teacher-ui-intake.sh --id TUI-001 --input /tmp/transkript.txt

Wirkung:
  - normalisiert eine Spracheingabe (Fuellwoerter reduzieren)
  - zerlegt die Eingabe in strukturierte Anforderungen
  - erzeugt To-do-Liste, Akzeptanzkriterien und Testvorschlaege
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
      echo "[intake] ERROR: Unbekanntes Argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$ID" ]]; then
  echo "[intake] ERROR: --id ist erforderlich" >&2
  usage
  exit 1
fi

INTAKE_DIR="generated/teacher-ui/intake"
mkdir -p "$INTAKE_DIR"

if [[ -z "$OUTPUT_FILE" ]]; then
  OUTPUT_FILE="$INTAKE_DIR/${ID}-structured.md"
fi

RAW_TEXT=""
if [[ -n "$INPUT_FILE" ]]; then
  if [[ ! -f "$INPUT_FILE" ]]; then
    echo "[intake] ERROR: Input-Datei nicht gefunden: $INPUT_FILE" >&2
    exit 1
  fi
  RAW_TEXT="$(cat "$INPUT_FILE")"
else
  RAW_TEXT="Lehrkraefte sollen Ideen per Sprache erfassen koennen. Die Eingabe wird transkribiert, sprachlich bereinigt und in einzelne Anforderungen zerlegt. Das System soll Zielgruppe, Prozess und passende UI-Zuordnung vorschlagen. Danach soll automatisch eine priorisierte To-do-Liste mit Akzeptanzkriterien und technischen Aufgaben erzeugt werden."
fi

NORMALIZED="$(echo "$RAW_TEXT" \
  | tr '\n' ' ' \
  | sed -E 's/\b(also|genau|halt|irgendwie|sozusagen|quasi|eigentlich)\b//gi' \
  | sed -E 's/[[:space:]]+/ /g' \
  | sed -E 's/^ //; s/ $//')"

REQ_TMP="$(mktemp)"
echo "$NORMALIZED" \
  | sed -E 's/[.;!?]+/\n/g' \
  | sed -E 's/^ +//; s/ +$//' \
  | awk 'length($0) > 12' > "$REQ_TMP"

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

{
  echo "# ${ID} Strukturierte Intake-Analyse"
  echo
  echo "Erstellt am (UTC): $timestamp"
  echo
  echo "## Normalisierte Eingabe"
  echo
  echo "$NORMALIZED"
  echo
  echo "## Erkannte Einzelanforderungen"
  echo
  n=1
  while IFS= read -r line; do
    echo "$n. $line"
    n=$((n+1))
  done < "$REQ_TMP"
  echo
  echo "## Standard To-do-Liste"
  echo
  echo "- [ ] Idee vollstaendig erfassen"
  echo "- [ ] Einzelanforderungen finalisieren"
  echo "- [ ] Zielgruppe und Rollen zuordnen"
  echo "- [ ] Prozesszuordnung bestaetigen"
  echo "- [ ] UI-Zuordnung mit Klickpfad pruefen"
  echo "- [ ] Dopplungen gegen bestehende UI pruefen"
  echo "- [ ] Prioritaet und Abhaengigkeiten festlegen"
  echo "- [ ] Akzeptanzkriterien definieren"
  echo "- [ ] Technische Teilaufgaben anlegen"
  echo "- [ ] Testfaelle spezifizieren"
  echo "- [ ] Datenschutz- und Sicherheitscheck einplanen"
  echo
  echo "## Akzeptanzkriterien"
  echo
  echo "1. Spracheingabe wird in weniger als 5 Sekunden in Klartext normalisiert."
  echo "2. Jede Eingabe wird in mindestens eine, maximal 15 Einzelanforderungen zerlegt."
  echo "3. Jede Einzelanforderung enthaelt Prozess- und Zielbereichszuordnung (Core/Course)."
  echo "4. Es wird automatisch eine priorisierte To-do-Liste erzeugt."
  echo "5. Akzeptanzkriterien und technische Teilaufgaben werden im Backlog gespeichert."
  echo "6. Unklare Angaben werden als offene Punkte markiert, nicht verworfen."
  echo
  echo "## Testvorschlaege"
  echo
  echo "- Parser-Test: Fuellwoerter entfernen ohne Bedeutungsverlust."
  echo "- Segmentierungs-Test: Lange Spracheingabe wird korrekt in Anforderungen geteilt."
  echo "- Mapping-Test: Prozess und Zielbereich werden fuer jede Anforderung gesetzt."
  echo "- Regressionstest: Leere oder sehr kurze Eingaben liefern klare Fehlermeldung."
} > "$OUTPUT_FILE"

rm -f "$REQ_TMP"

echo "[intake] OK: Strukturdatei erzeugt: $OUTPUT_FILE"