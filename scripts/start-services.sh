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

docker compose up -d --build

echo "[start] Warte auf MySQL-Init und python-api..."
sleep 5
docker compose restart python-api >/dev/null 2>&1 || true

echo "[start] Dienste gestartet"
echo "[start] PHP-Webapp:   http://localhost:${PHP_WEB_PORT:-8080}"
echo "[start] Python-API:   http://localhost:${PYTHON_API_PORT:-8000}/health"
