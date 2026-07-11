#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT_DIR"

REPORT_DIR="generated/weiter-status-history"
LATEST_REPORT="generated/weiter-status.md"
mkdir -p "$REPORT_DIR"

timestamp="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
safe_stamp="$(date -u +"%Y%m%d-%H%M%S")"
report_file="$REPORT_DIR/weiter-status-$safe_stamp.md"

branch="$(git branch --show-current 2>/dev/null || echo unknown)"
last_commit="$(git log --oneline -n 1 2>/dev/null || echo 'no commits')"

status_short="$(git status --short 2>/dev/null || true)"
if [[ -z "$status_short" ]]; then
  working_tree="clean"
else
  working_tree="dirty"
fi

ahead=0
behind=0
if git rev-parse --abbrev-ref --symbolic-full-name "@{u}" >/dev/null 2>&1; then
  ahead_behind="$(git rev-list --left-right --count "@{u}"...HEAD 2>/dev/null || echo '0 0')"
  read -r behind ahead <<< "$(echo "$ahead_behind" | tr -s ' ')"
fi

has_marker() {
  local pattern="$1"
  shift
  if grep -RIn -- "$pattern" "$@" >/dev/null 2>&1; then
    echo yes
  else
    echo no
  fi
}

hint_api="$(has_marker '/api/.*/assistant/hint|/api/v1/assistant/hint' services/python-api/learning_api webapp/public/js/controllers/assistant.controller.mjs)"
hint_ui="$(has_marker 'assistantHintBox|assistant.controller.mjs|data-course-action="hint"' webapp/public/index.php webapp/public/js webapp/public/style.css)"
keyword_search="$(has_marker 'assistant/keyword-search|keyword_search_route|Stichwortsuche' services/python-api/learning_api webapp/public)"
w3schools_source="$(has_marker 'w3schools.com/sql' services/python-api/learning_api/keyword_knowledge.py)"
audit_trail="$(has_marker 'assistant_interactions|assistant_repository|response_hint' services/python-api/learning_api)"
teacher_features="$(has_marker 'teacher_note|Lehrkraft|teacher' services/python-api/learning_api webapp/public docs/handbuch)"

m1_baseline="no"
if [[ "$working_tree" == "clean" && "$ahead" -eq 0 && "$behind" -eq 0 ]]; then
  m1_baseline="yes"
fi

m2_hint="no"
if [[ "$hint_api" == "yes" && "$hint_ui" == "yes" ]]; then
  m2_hint="yes"
fi

m3_knowledge="no"
if [[ "$keyword_search" == "yes" && "$w3schools_source" == "yes" ]]; then
  m3_knowledge="yes"
fi

m4_audit="no"
if [[ "$audit_trail" == "yes" ]]; then
  m4_audit="yes"
fi

m5_teacher="no"
if [[ "$teacher_features" == "yes" ]]; then
  m5_teacher="yes"
fi

next_milestone=""
next_actions=""

if [[ "$m1_baseline" == "no" ]]; then
  next_milestone="M1 Baseline sichern"
  next_actions=$'- Lokale Aenderungen committen und pushen.\n- Optionalen Snapshot-Tag setzen.\n- Danach erneut bash scripts/weiter.sh ausfuehren.'
elif [[ "$m2_hint" == "no" ]]; then
  next_milestone="M2 Hint-Modus abschliessen"
  next_actions=$'- API-Endpunkt und UI-Hinweisdialog vervollstaendigen.\n- Hint-Policy (keine Vollloesung) absichern.\n- API + UI Smoke-Test ausfuehren.'
elif [[ "$m3_knowledge" == "no" ]]; then
  next_milestone="M3 Wissensanbindung RDB abschliessen"
  next_actions=$'- Wissensindex + Quellenprovenienz vervollstaendigen.\n- Stichwortsuche mit Beispielkarten absichern.\n- Quellenpriorisierung dokumentieren.'
elif [[ "$m4_audit" == "no" ]]; then
  next_milestone="M4 Audit-Trail absichern"
  next_actions=$'- Interaktionslogging mit Feldern fuer Quelle und Hinweis sichern.\n- Export/Review-Prozess fuer Lehrkraefte dokumentieren.\n- Datenschutzpruefung aktualisieren.'
elif [[ "$m5_teacher" == "no" ]]; then
  next_milestone="M5 Lehrkraftmodus ausbauen"
  next_actions=$'- Lehrkraft-Workflows fuer Aufgaben/Bewertung priorisieren.\n- Rollenrechte und UI-Zuordnung je Prozess klar trennen.\n- Abhaengigkeiten zwischen Course und Core dokumentieren.'
else
  next_milestone="M6 Schulbetrieb-Features starten"
  next_actions=$'- Avatar-/Voice-/DSGVO-Backlog in Teilaufgaben aufteilen.\n- Governance fuer Prompt-, Wissens- und Modellupdates festlegen.\n- Pilotbetrieb mit Feedbackzyklus vorbereiten.'
fi

cat > "$report_file" <<EOF
# Weiter-Statusbericht

Zeitpunkt (UTC): $timestamp

## Repo-Stand

- Branch: $branch
- Letzter Commit: $last_commit
- Working Tree: $working_tree
- Ahead/Behind gegen Upstream: ahead=$ahead, behind=$behind

## Auto-Erkennung nach Marschplan

- M1 Baseline gesichert: $m1_baseline
- M2 Hint-Modus (API + UI): $m2_hint
- M3 Wissensanbindung (Suche + Quellen): $m3_knowledge
- M4 Audit-Trail: $m4_audit
- M5 Lehrkraft-Features Fundament: $m5_teacher

## Analyse-Dimensionen

### Best Practice
- SSOT-Dokumentation und Pflicht-Gates weiterhin als Abschlussregel verwenden.
- Aenderungen nur in klar getrennten Schichten (Route/Service/Repository/UI).

### Prozess
- Naechster Milestone wird datenbasiert aus Marker-Status ermittelt.
- Jeder Lauf erzeugt einen neuen Statusbericht als Audit-Artefakt.

### Zuordnung (Core vs Course)
- Core: wiederverwendbare Assistentenlogik, Sicherheitsregeln, Logging, Rollenmodell.
- Course: fachspezifische Inhalte, Aufgabenkarten, didaktische Beispiele.

### Usability
- Funktionen pro Arbeitsprozess gruppieren (nicht pro Technikmodul).
- Neue Funktionen zuerst in bestehende Reiter/Views einordnen, neue Hauptreiter nur bei klarer Eigenstaendigkeit.

## Naechster Milestone

$next_milestone

## Naechste Schritte

$next_actions

## Sinnvolle Testvorschlaege fuer den naechsten Zyklus

- API-Tests: Hint-Endpunkt, Keyword-Search, Fehlerpfade.
- UI-Smoke: Laden, Weiter-Navigation, Lernhilfe, Stichwortsuche.
- Sicherheits-Checks: SQL-Sandbox-Write-Blocker, Input-Validierung, Fehlerausgaben.
- Pflicht-Gates: bash scripts/validate-security.sh, bash scripts/validate-architecture.sh, bash scripts/validate-docs.sh.
EOF

cp "$report_file" "$LATEST_REPORT"

echo "[weiter] Statusbericht erstellt: $report_file"
echo "[weiter] Aktueller Bericht: $LATEST_REPORT"
echo "[weiter] Naechster Milestone: $next_milestone"
