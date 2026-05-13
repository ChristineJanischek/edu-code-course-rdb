#!/usr/bin/env bash
set -euo pipefail

input_dir="generated/klassenarbeiten"
output_guide="${input_dir}/WORKBENCH-MWB-WORKFLOW.md"
only_system=""
db_prefix="wb_"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --input-dir)
      input_dir="$2"
      shift 2
      ;;
    --output-guide)
      output_guide="$2"
      shift 2
      ;;
    --only-system)
      only_system="$2"
      shift 2
      ;;
    --db-prefix)
      db_prefix="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Verwendung:
  bash scripts/prepare-workbench-mwb.sh [Optionen]

Optionen:
  --input-dir <pfad>      Verzeichnis mit *_struktur_*.sql (Default: generated/klassenarbeiten)
  --output-guide <pfad>   Zieldatei fuer den Workbench-Workflow (Default: generated/klassenarbeiten/WORKBENCH-MWB-WORKFLOW.md)
  --only-system <name>    Nur ein System verarbeiten (z. B. stadtfahrradverleih)
  --db-prefix <prefix>    Prefix fuer erzeugte Datenbanken (Default: wb_)
  -h, --help              Hilfe anzeigen

Ergebnis:
  1) SQL-Struktur + SQL-Daten werden in getrennte DB-Schemas geladen.
  2) Eine Anleitung fuer MySQL Workbench wird erzeugt, um daraus echte .mwb zu speichern.
EOF
      exit 0
      ;;
    *)
      echo "[prepare-mwb] Unbekannte Option: $1"
      exit 1
      ;;
  esac
done

if [[ ! -d "$input_dir" ]]; then
  echo "[prepare-mwb] Fehler: Eingabeverzeichnis nicht gefunden: $input_dir"
  exit 1
fi

runtime_root_pw="${MYSQL_ROOT_PASSWORD:-}"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  source .env
  set +a
fi

if [[ -n "$runtime_root_pw" ]]; then
  MYSQL_ROOT_PASSWORD="$runtime_root_pw"
fi

if [[ -z "${MYSQL_ROOT_PASSWORD:-}" || "${MYSQL_ROOT_PASSWORD}" == CHANGE_ME* ]]; then
  echo "[prepare-mwb] Fehler: MYSQL_ROOT_PASSWORD fehlt oder ist ungueltig."
  echo "[prepare-mwb] Bitte .env konfigurieren oder MYSQL_ROOT_PASSWORD als Umgebungsvariable setzen."
  exit 1
fi

if ! command -v docker >/dev/null 2>&1; then
  echo "[prepare-mwb] Fehler: docker nicht gefunden."
  exit 1
fi

if ! docker compose ps --status running --services 2>/dev/null | grep -qx "mysql"; then
  echo "[prepare-mwb] Fehler: MySQL-Container laeuft nicht."
  echo "[prepare-mwb] Tipp: bash scripts/start-services.sh"
  exit 1
fi

sanitize_identifier() {
  local value="$1"
  value="${value,,}"
  value="$(echo "$value" | tr -cs 'a-z0-9_' '_')"
  value="${value#_}"
  value="${value%_}"
  echo "$value"
}

rewrite_sql_for_database() {
  local source_file="$1"
  local target_db="$2"
  local target_file="$3"

  awk -v db="$target_db" '
  {
    if ($0 ~ /^[[:space:]]*DROP[[:space:]]+DATABASE[[:space:]]+IF[[:space:]]+EXISTS[[:space:]]+/) {
      print "DROP DATABASE IF EXISTS " db ";"
      next
    }
    if ($0 ~ /^[[:space:]]*CREATE[[:space:]]+DATABASE[[:space:]]+/) {
      print "CREATE DATABASE " db " CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;"
      next
    }
    if ($0 ~ /^[[:space:]]*USE[[:space:]]+/) {
      print "USE " db ";"
      next
    }
    print $0
  }
  ' "$source_file" > "$target_file"
}

tmp_dir="$(mktemp -d)"
trap 'rm -rf "$tmp_dir"' EXIT

host_for_workbench="${MYSQL_HOST:-127.0.0.1}"
if [[ "$host_for_workbench" == "mysql" ]]; then
  host_for_workbench="127.0.0.1"
fi
port_for_workbench="${MYSQL_PORT:-3306}"
user_for_workbench="root"

entries=""
processed=0
errors=0

for struct_sql in "$input_dir"/*_struktur_*.sql; do
  [[ -e "$struct_sql" ]] || continue

  filename="$(basename "$struct_sql")"
  system_name="${filename%_struktur_*}"
  year_part="${filename##*_struktur_}"
  year="${year_part%.sql}"

  if [[ -n "$only_system" ]] && [[ "$system_name" != "$only_system" ]]; then
    continue
  fi

  data_sql="$input_dir/${system_name}_daten_${year}.sql"
  if [[ ! -f "$data_sql" ]]; then
    echo "[prepare-mwb] WARN: Daten-Datei fehlt, uebersprungen: $data_sql"
    errors=$((errors + 1))
    continue
  fi

  target_mwb="$input_dir/${system_name}_${year}.mwb"
  target_db_raw="${db_prefix}${system_name}_${year}"
  target_db="$(sanitize_identifier "$target_db_raw")"

  rewritten_struct="$tmp_dir/${system_name}_${year}_struktur.sql"
  rewritten_data="$tmp_dir/${system_name}_${year}_daten.sql"

  rewrite_sql_for_database "$struct_sql" "$target_db" "$rewritten_struct"
  rewrite_sql_for_database "$data_sql" "$target_db" "$rewritten_data"

  echo "[prepare-mwb] Importiere: ${system_name} (${year}) -> DB ${target_db}"
  docker compose exec -T mysql mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < "$rewritten_struct"
  docker compose exec -T mysql mysql -uroot -p"${MYSQL_ROOT_PASSWORD}" < "$rewritten_data"

  table_count=$(docker compose exec -T mysql mysql -N -B -uroot -p"${MYSQL_ROOT_PASSWORD}" -e "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='${target_db}';" | tr -d '\r')
  if [[ -z "$table_count" ]]; then
    table_count="0"
  fi

  entries+="$(printf '| %s | %s | %s | %s | %s | %s | %s |' "$system_name" "$year" "$target_db" "$table_count" "$struct_sql" "$data_sql" "$target_mwb")"
  entries+=$'\n'
  processed=$((processed + 1))
done

if [[ $processed -eq 0 ]]; then
  echo "[prepare-mwb] Fehler: Keine verarbeitbaren *_struktur_*.sql Dateien fuer Guide-Erstellung gefunden."
  exit 1
fi

cat > "$output_guide" <<EOF
# Workflow: Echte MySQL Workbench .mwb aus SQL erzeugen

Diese Datei wurde automatisch erzeugt mit:

\`bash scripts/prepare-workbench-mwb.sh\`

## 1) Vorbereitete Datenbankschemata

| System | Jahr | Schema fuer Reverse Engineering | Tabellen | Struktur-SQL | Daten-SQL | Ziel-.mwb |
|---|---:|---|---:|---|---|---|
${entries}

## 2) Schritte in MySQL Workbench (pro System)

1. Workbench starten.
2. Verbindung anlegen/waehlen mit diesen Parametern:
   - Hostname: ${host_for_workbench}
   - Port: ${port_for_workbench}
   - Username: ${user_for_workbench}
3. Menue: \`Database -> Reverse Engineer...\`
4. Das passende Schema aus der Tabelle oben auswaehlen.
5. Import abschliessen, dann im Modell auf EER-Diagramm wechseln.
6. Notation setzen: \`Model -> Relationship Notation -> Connect to Columns\` (wenn verfuegbar).
7. Speichern: \`File -> Save Model As...\` und die Datei auf den jeweiligen Ziel-.mwb-Pfad speichern.

## 3) Validierung einer echten .mwb

Eine echte Workbench-Datei enthaelt intern die Datei \`document.mwb.xml\`.

Beispielpruefung:

\`unzip -l <datei>.mwb | grep document.mwb.xml\`

Wenn kein Treffer kommt, ist die Datei kein natives Workbench-Modell.
EOF

echo "[prepare-mwb] Fertig: ${processed} System(e) vorbereitet"
echo "[prepare-mwb] Guide: ${output_guide}"

if [[ $errors -gt 0 ]]; then
  echo "[prepare-mwb] Hinweis: ${errors} System(e) wegen fehlender Daten-Datei uebersprungen"
fi
