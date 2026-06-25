#!/usr/bin/env bash
set -euo pipefail

fail=0

note_fail() {
  echo "[security] FAIL: $1"
  fail=1
}

search() {
  local pattern="$1"
  shift
  grep -nE "$pattern" "$@" >/dev/null 2>&1
}

print_matches() {
  local pattern="$1"
  shift
  grep -nE "$pattern" "$@" || true
}

echo "[security] Starte Sicherheitsvalidierung..."

if git ls-files --error-unmatch .env >/dev/null 2>&1 && [[ -f .env ]]; then
  note_fail ".env ist versioniert. Lokale Secrets duerfen nicht im Repo liegen."
fi

mapfile -t python_api_files < <(find services/python-api -type f -name "*.py" | sort)

if search "MYSQL_ROOT_PASSWORD=root|MYSQL_PASSWORD=apppassword" docker-compose.yml .env.example "${python_api_files[@]}"; then
  print_matches "MYSQL_ROOT_PASSWORD=root|MYSQL_PASSWORD=apppassword" docker-compose.yml .env.example "${python_api_files[@]}"
  note_fail "Unsichere Default-Credentials gefunden."
fi

if search '"error": str\(exc\)' "${python_api_files[@]}"; then
  note_fail "Interne Exceptions werden ungefiltert an API-Clients geleakt."
fi

if [[ $fail -ne 0 ]]; then
  echo "[security] Sicherheitsvalidierung fehlgeschlagen"
  exit 1
fi

echo "[security] Sicherheitsvalidierung erfolgreich"
