#!/usr/bin/env bash
set -euo pipefail

fail=0

note_fail() {
  echo "[arch] FAIL: $1"
  fail=1
}

echo "[arch] Starte Architekturvalidierung..."

# Java-Basis-Check
./scripts/test-java.sh

# OOP-Guardrails: Keine mutierenden Setter fuer interne Teamlisten
if grep -nE "setStartaufstellung\(|setErsatzBank\(" src/volleyball/VolleyballspielerTeamManager.java >/dev/null 2>&1; then
  note_fail "Model kapselt interne Listen nicht sauber (mutierende Setter gefunden)."
fi

# Null-Sentinel im Model vermeiden
if grep -nE "default:[[:space:]]*return[[:space:]]+null;" src/volleyball/VolleyballspielerTeamManager.java >/dev/null 2>&1; then
  note_fail "Model liefert null als Kontrollflusswert (bitte leere Sammlung/Exception nutzen)."
fi

# Python-API: app.py bleibt Bootstrap, Business-Logik liegt in learning_api/
if [[ ! -f services/python-api/learning_api/routes.py ]]; then
  note_fail "Python-API MVC-Struktur fehlt: services/python-api/learning_api/routes.py nicht gefunden."
fi

if [[ ! -f services/python-api/learning_api/submission_service.py ]]; then
  note_fail "Python-API Service-Schicht fehlt: services/python-api/learning_api/submission_service.py nicht gefunden."
fi

if grep -nE "@app\.|def normalize_submission_payload\(" services/python-api/app.py >/dev/null 2>&1; then
  note_fail "services/python-api/app.py enthaelt Business-Logik oder Route-Definitionen statt reinem Bootstrap."
fi

# Webapp: app.js bleibt Entry-Point ohne Business-Logik
if grep -nE "class |function " webapp/public/app.js >/dev/null 2>&1; then
  note_fail "webapp/public/app.js soll nur Bootstrap-Code enthalten. Business-Logik in webapp/public/js/*.mjs auslagern."
fi

if [[ $fail -ne 0 ]]; then
  echo "[arch] Architekturvalidierung fehlgeschlagen"
  exit 1
fi

echo "[arch] Architekturvalidierung erfolgreich"
