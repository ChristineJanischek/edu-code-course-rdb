#!/usr/bin/env bash
set -euo pipefail

# .env laden falls vorhanden, damit alle Variablen gesetzt sind
if [[ -f .env ]]; then
  set -a
  # shellcheck source=.env
  source .env
  set +a
fi

python_port="${PYTHON_API_PORT:-8000}"
php_port="${PHP_WEB_PORT:-8080}"

function require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "[test] Fehler: Kommando '$1' fehlt"
    exit 1
  fi
}

require_cmd curl
require_cmd docker

echo "[test] Pruefe Python-Health..."
for attempt in {1..20}; do
  if curl -fsS "http://localhost:${python_port}/api/v1/health" >/tmp/python_health.json; then
    break
  fi

  if [[ "$attempt" == "20" ]]; then
    echo "[test] Fehler: Python-Health-Endpunkt nicht erreichbar."
    exit 1
  fi

  echo "[test] Python-API noch nicht bereit (Versuch ${attempt}/20)"
  sleep 1
done

cat /tmp/python_health.json
grep -q '"ok":true' /tmp/python_health.json || {
  echo "[test] Fehler: Python-API meldet keine erfolgreiche MySQL-Verbindung"
  exit 1
}

echo "[test] Pruefe Schutz fuer sensitive API-Endpunkte..."
direct_submission_status="$(curl -s -o /tmp/direct_submission_response.json -w '%{http_code}' \
  -X POST "http://localhost:${python_port}/api/v1/submissions" \
  -H 'Content-Type: application/json' \
  -d '{"learner_alias":"probe","task_id":"probe_task","response_text":"test","response_kind":"text"}')"
if [[ "$direct_submission_status" != "401" ]]; then
  echo "[test] Fehler: Direkter Zugriff auf /api/v1/submissions ist nicht abgesichert (Status ${direct_submission_status})."
  cat /tmp/direct_submission_response.json
  exit 1
fi

echo "[test] Pruefe Python-JSON..."
curl -fsS "http://localhost:${python_port}/api/v1/json-items" >/tmp/python_json.json
cat /tmp/python_json.json

echo "[test] Pruefe Lehrplan-API..."
curl -fsS "http://localhost:${python_port}/api/v1/curricula" >/tmp/curricula.json
cat /tmp/curricula.json
grep -q '"documents"' /tmp/curricula.json || {
  echo "[test] Fehler: Lehrplan-API liefert keine Dokumentliste"
  exit 1
}

echo "[test] Pruefe PHP-Webseite..."
curl -fsS "http://localhost:${php_port}" >/tmp/php_index.html
head -n 5 /tmp/php_index.html
if grep -Eqi 'Fatal error|Warning:|Notice:' /tmp/php_index.html; then
  echo "[test] Fehler: PHP-Webseite liefert Laufzeitfehler"
  exit 1
fi

echo "[test] Pruefe PHP-API-Proxy..."
curl -fsS "http://localhost:${php_port}/api-proxy.php/api/v1/health" >/tmp/php_proxy_health.json
cat /tmp/php_proxy_health.json
grep -q '"success":true' /tmp/php_proxy_health.json || {
  echo "[test] Fehler: PHP-Proxy liefert keinen erfolgreichen API-Response"
  exit 1
}

echo "[test] Pruefe Schueler-Dokumente aus generated/..."
curl -fsS "http://localhost:${php_port}/generated/anleitungen/stoffverlaufsplan_rdb_3wochen.html" >/tmp/generated_plan.html
grep -qi '<html' /tmp/generated_plan.html || {
  echo "[test] Fehler: Stoffverlaufsplan ist ueber die Webapp nicht erreichbar"
  exit 1
}

echo "[test] Pruefe MySQL in Container..."
docker compose exec -T mysql mysql -u"${MYSQL_USER:-appuser}" -p"${MYSQL_PASSWORD:-apppassword}" "${MYSQL_DATABASE:-appdb}" -e "SELECT COUNT(*) AS demo_items_count FROM demo_items;"

echo "[test] Starte Java-Smoke-Test..."
./scripts/test-java.sh

echo "[test] Alle Checks erfolgreich"
