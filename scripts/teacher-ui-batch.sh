#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

usage() {
  cat <<'EOF'
Nutzung:
  bash scripts/teacher-ui-batch.sh <batch-id>

Beispiel:
  bash scripts/teacher-ui-batch.sh BATCH-001

Wirkung:
  - erstellt eine Batch-Datei unter generated/teacher-ui/batches/
  - erstellt eine strukturierte Analyse unter generated/teacher-ui/analysen/
  - erzeugt einen backlog-ueberblick unter generated/teacher-ui/backlog/
EOF
}

if [[ "${1:-}" == "" || "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
fi

BATCH_ID="$1"
timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
safe_stamp="$(date -u +"%Y%m%d-%H%M%S")"

BATCH_DIR="generated/teacher-ui/batches"
ANALYSIS_DIR="generated/teacher-ui/analysen"
BACKLOG_DIR="generated/teacher-ui/backlog"

mkdir -p "$BATCH_DIR" "$ANALYSIS_DIR" "$BACKLOG_DIR"

batch_file="$BATCH_DIR/${BATCH_ID}.md"
analysis_file="$ANALYSIS_DIR/${BATCH_ID}-analyse.md"
backlog_file="$BACKLOG_DIR/TEACHER_UI_MASTER_BACKLOG.md"

if [[ -f "$batch_file" ]]; then
  echo "[batch] WARN: Batch-Datei existiert bereits: $batch_file"
else
  cat > "$batch_file" <<EOF
# $BATCH_ID

Erfasst am (UTC): $timestamp

## Eingaben

1. Titel:
2. Freitext oder Sprachtranskript:
3. Prioritaet (Kritisch/Hoch/Mittel/Niedrig):
4. Zielbereich (Core/Course/Unklar):
5. Betroffener Prozess:
6. Optionaler UI-Bereich:

## Hinweise

- Eine Batch kann mehrere Ideen enthalten.
- Jede Idee spaeter als eigene TUI-Anforderung auspraegen.
EOF
  echo "[batch] OK: Batch-Datei erstellt: $batch_file"
fi

cat > "$analysis_file" <<EOF
# Analyse $BATCH_ID

Zeitpunkt (UTC): $timestamp

## Best Practice

- Jede Idee getrennt als eindeutige TUI-Anforderung fuehren.
- Vor Implementierung Dopplungen zu bestehender UI pruefen.

## Prozess

- Idee erfassen
- Zielgruppe und Prozess zuordnen
- UI-Platzierung bestimmen
- Akzeptanzkriterien formulieren
- technische Teilaufgaben priorisieren

## Zuordnung

- Core: wiederverwendbare UI-Logik, Rollen, Berechtigungen, Konfigurationsassistenten.
- Course: kursbezogene Inhalte, aufgabennahe Assistenz, fachspezifische Defaults.

## Usability

- Erst in bestehende Reiter/Fenster integrieren.
- Neue Hauptreiter nur bei eigenstaendigem Arbeitsprozess.
- Maximal kurze Klickpfade fuer haeufige Aufgaben.

## Nächster Schritt

- Batch in einzelne TUI-Backlogeintraege ueberfuehren.
EOF
echo "[batch] OK: Analyse erstellt: $analysis_file"

if [[ ! -f "$backlog_file" ]]; then
  cat > "$backlog_file" <<EOF
# Teacher UI Master Backlog

Aktualisiert am (UTC): $timestamp

## Batches

- $BATCH_ID (erstellt $safe_stamp)
EOF
else
  printf "\n- %s (erstellt %s)\n" "$BATCH_ID" "$safe_stamp" >> "$backlog_file"
fi

echo "[batch] OK: Backlog aktualisiert: $backlog_file"