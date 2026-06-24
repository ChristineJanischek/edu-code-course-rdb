#!/usr/bin/env bash
set -euo pipefail

if [[ ! -f .env ]]; then
  cp .env.example .env
  echo "[start] .env aus .env.example erzeugt"
fi

# Preserve explicit runtime values before reading .env placeholders.
runtime_root_pw="${MYSQL_ROOT_PASSWORD:-}"
runtime_app_pw="${MYSQL_PASSWORD:-}"

set -a
# shellcheck disable=SC1091
source .env
set +a

if [[ -n "$runtime_root_pw" ]]; then
  MYSQL_ROOT_PASSWORD="$runtime_root_pw"
fi
if [[ -n "$runtime_app_pw" ]]; then
  MYSQL_PASSWORD="$runtime_app_pw"
fi

if [[ -z "${MYSQL_ROOT_PASSWORD:-}" || -z "${MYSQL_PASSWORD:-}" || "${MYSQL_ROOT_PASSWORD}" == CHANGE_ME* || "${MYSQL_PASSWORD}" == CHANGE_ME* ]]; then
  echo "[start] Fehler: Es fehlen gueltige MySQL-Passwoerter."
  echo "[start] Setze MYSQL_ROOT_PASSWORD und MYSQL_PASSWORD in .env oder als Umgebungsvariablen."
  exit 1
fi

if [[ -z "${SUBMISSION_API_KEY:-}" || "${SUBMISSION_API_KEY}" == CHANGE_ME* ]]; then
  echo "[start] Fehler: SUBMISSION_API_KEY ist nicht sicher konfiguriert."
  echo "[start] Setze in .env einen starken Wert fuer SUBMISSION_API_KEY."
  exit 1
fi

docker compose up -d --build

echo "[start] Warte auf MySQL-Init und python-api..."
docker compose restart python-api >/dev/null 2>&1 || true

python_port="${PYTHON_API_PORT:-8000}"
for attempt in {1..30}; do
  if curl -fsS "http://localhost:${python_port}/health" | grep -q '"ok":true'; then
    break
  fi
  echo "[start] API noch nicht bereit (Versuch ${attempt}/30)"
  if [[ "$attempt" == "30" ]]; then
    echo "[start] Fehler: Python-API meldet MySQL noch nicht als bereit."
    exit 1
  fi
  sleep 2
done

echo "[start] Dienste gestartet"
echo "[start] PHP-Webapp:   http://localhost:${PHP_WEB_PORT:-8080}"
echo "[start] Python-API:   http://localhost:${PYTHON_API_PORT:-8000}/api/v1/health"
echo "[start] PHP-Proxy:    http://localhost:${PHP_WEB_PORT:-8080}/api-proxy.php/api/v1/health"

if [[ -n "${CODESPACE_NAME:-}" ]]; then
  echo "[start] Codespace-Webapp: https://${CODESPACE_NAME}-${PHP_WEB_PORT:-8080}.app.github.dev"
  echo "[start] Codespace-API:    https://${CODESPACE_NAME}-${PYTHON_API_PORT:-8000}.app.github.dev/api/v1/health"
fi
