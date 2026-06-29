from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass
from pathlib import Path
from threading import Lock
from typing import Any

import pymysql

from .db import db_connection

MAX_ROWS = 200
MAX_SQL_LENGTH = 12000

_WRITE_KEYWORDS = {
    "INSERT",
    "UPDATE",
    "DELETE",
    "DROP",
    "ALTER",
    "CREATE",
    "TRUNCATE",
    "REPLACE",
    "GRANT",
    "REVOKE",
    "LOCK",
    "UNLOCK",
    "SET",
    "USE",
    "CALL",
    "DO",
    "HANDLER",
    "LOAD",
    "OUTFILE",
    "INFILE",
    "RENAME",
}

_ALLOWED_START = ("SELECT", "WITH")


@dataclass(frozen=True)
class SandboxDataset:
    key: str
    database_name: str
    structure_path: Path
    data_path: Path


_SANDBOX_LOCK = Lock()


def _repo_root() -> Path:
    configured = os.getenv("REPO_ROOT")
    if configured:
        return Path(configured).resolve()

    # In the container runtime the module path is /app/learning_api/*.py.
    # parents[1] resolves to /app and keeps local workspace compatibility.
    return Path(__file__).resolve().parents[1]


def _dataset_registry() -> dict[str, SandboxDataset]:
    root = _repo_root()

    return {
        "foodtrucknetz_uebung": SandboxDataset(
            key="foodtrucknetz_uebung",
            database_name="sandbox_foodtrucknetz_uebung",
            structure_path=root / "generated/klassenarbeiten/foodtrucknetz_struktur_2025.sql",
            data_path=root / "generated/uebungen/daten/foodtrucknetz_uebung_daten.sql",
        ),
        "stadtfahrradverleih_uebung": SandboxDataset(
            key="stadtfahrradverleih_uebung",
            database_name="sandbox_stadtfahrradverleih_uebung",
            structure_path=root / "generated/klassenarbeiten/stadtfahrradverleih_struktur_2025.sql",
            data_path=root / "generated/uebungen/daten/stadtfahrradverleih_uebung_daten.sql",
        ),
        "stadtfahrradverleih_ka": SandboxDataset(
            key="stadtfahrradverleih_ka",
            database_name="sandbox_stadtfahrradverleih_ka",
            structure_path=root / "generated/klassenarbeiten/stadtfahrradverleih_struktur_2025.sql",
            data_path=root / "generated/klassenarbeiten/stadtfahrradverleih_daten_2025.sql",
        ),
        "foodtrucknetz_ka": SandboxDataset(
            key="foodtrucknetz_ka",
            database_name="sandbox_foodtrucknetz_ka",
            structure_path=root / "generated/klassenarbeiten/foodtrucknetz_struktur_2025.sql",
            data_path=root / "generated/klassenarbeiten/foodtrucknetz_daten_2025.sql",
        ),
        "coworkingcampus_ka": SandboxDataset(
            key="coworkingcampus_ka",
            database_name="sandbox_coworkingcampus_ka",
            structure_path=root / "generated/klassenarbeiten/coworkingcampus_struktur_2025.sql",
            data_path=root / "generated/klassenarbeiten/coworkingcampus_daten_2025.sql",
        ),
    }


def _dataset_fingerprint(dataset: SandboxDataset) -> str:
    structure_content = dataset.structure_path.read_text(encoding="utf-8")
    data_content = dataset.data_path.read_text(encoding="utf-8")
    digest = hashlib.sha256()
    digest.update(structure_content.encode("utf-8"))
    digest.update(data_content.encode("utf-8"))
    return digest.hexdigest()


def _cleanup_sql_script(sql: str, target_db: str) -> str:
    rewritten = sql
    rewritten = re.sub(r"^\s*--.*$", "", rewritten, flags=re.MULTILINE)
    rewritten = re.sub(r"/\*![\s\S]*?\*/", "", rewritten)
    rewritten = re.sub(r"^\s*USE\s+[^;]+;", "", rewritten, flags=re.IGNORECASE | re.MULTILINE)
    rewritten = re.sub(r"^\s*DROP\s+DATABASE\s+IF\s+EXISTS\s+[^;]+;", "", rewritten, flags=re.IGNORECASE | re.MULTILINE)
    rewritten = re.sub(r"^\s*CREATE\s+DATABASE\s+[^;]+;", "", rewritten, flags=re.IGNORECASE | re.MULTILINE)
    return f"USE `{target_db}`;\n{rewritten}"


def _split_statements(script: str) -> list[str]:
    statements: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escaped = False

    for char in script:
        current.append(char)
        if escaped:
            escaped = False
            continue

        if char == "\\":
            escaped = True
            continue

        if quote:
            if char == quote:
                quote = None
            continue

        if char in ("'", '"', "`"):
            quote = char
            continue

        if char == ";":
            statement = "".join(current).strip()
            if statement:
                statements.append(statement)
            current = []

    tail = "".join(current).strip()
    if tail:
        statements.append(tail)

    return statements


def _open_admin_connection() -> tuple[pymysql.connections.Connection | None, dict[str, Any] | None]:
    host = os.getenv("MYSQL_HOST", "mysql")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "appuser")
    password = os.getenv("MYSQL_PASSWORD", "")

    if not password:
        return None, {"error": "MYSQL_PASSWORD not configured"}

    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            connect_timeout=5,
            charset="utf8mb4",
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor,
        )
    except Exception:
        return None, {"error": "Database connection failed"}

    return connection, None


def _ensure_dataset(dataset: SandboxDataset) -> tuple[bool, str | None]:
    if not dataset.structure_path.exists() or not dataset.data_path.exists():
        return False, "Sandbox dataset files are missing"

    fingerprint = _dataset_fingerprint(dataset)

    admin_connection, admin_error = _open_admin_connection()
    if admin_connection is None:
        return False, (admin_error or {}).get("error", "Database connection failed")

    try:
        with admin_connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{dataset.database_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci")
            cursor.execute(f"USE `{dataset.database_name}`")
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sandbox_meta (
                    dataset_key VARCHAR(64) PRIMARY KEY,
                    fingerprint CHAR(64) NOT NULL,
                    loaded_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                )
                """
            )
            cursor.execute(
                "SELECT fingerprint FROM sandbox_meta WHERE dataset_key = %s",
                (dataset.key,),
            )
            row = cursor.fetchone()

        if row and row.get("fingerprint") == fingerprint:
            return True, None

        structure_sql = _cleanup_sql_script(dataset.structure_path.read_text(encoding="utf-8"), dataset.database_name)
        data_sql = _cleanup_sql_script(dataset.data_path.read_text(encoding="utf-8"), dataset.database_name)
        statements = _split_statements(structure_sql + "\n" + data_sql)

        with admin_connection.cursor() as cursor:
            for statement in statements:
                if not statement or statement == ";":
                    continue
                cursor.execute(statement)

            cursor.execute(
                """
                INSERT INTO sandbox_meta (dataset_key, fingerprint)
                VALUES (%s, %s)
                ON DUPLICATE KEY UPDATE fingerprint = VALUES(fingerprint)
                """,
                (dataset.key, fingerprint),
            )

        return True, None
    except Exception:
        return False, "Sandbox dataset could not be prepared"
    finally:
        admin_connection.close()


def validate_sql_readonly(sql: str) -> tuple[bool, str | None]:
    raw = str(sql or "").strip()
    if not raw:
        return False, "SQL query is empty"

    if len(raw) > MAX_SQL_LENGTH:
        return False, "SQL query is too long"

    stripped = re.sub(r"--.*$", "", raw, flags=re.MULTILINE)
    stripped = re.sub(r"/\*[\s\S]*?\*/", " ", stripped)
    stripped = stripped.strip()

    if not stripped:
        return False, "SQL query is empty"

    if stripped.count(";") > 1 or (";" in stripped and not stripped.rstrip().endswith(";")):
        return False, "Only one SQL statement is allowed"

    without_trailing = stripped[:-1].strip() if stripped.endswith(";") else stripped
    normalized_upper = without_trailing.upper()

    if not normalized_upper.startswith(_ALLOWED_START):
        return False, "Only SELECT/CTE statements are allowed"

    for keyword in _WRITE_KEYWORDS:
        pattern = re.compile(rf"\b{keyword}\b", re.IGNORECASE)
        if pattern.search(normalized_upper):
            return False, f"Forbidden SQL keyword: {keyword}"

    return True, None


def _run_select_query(dataset: SandboxDataset, sql: str) -> tuple[list[str], list[list[Any]], str | None]:
    connection, error_payload = db_connection()
    if connection is None:
        return [], [], (error_payload or {}).get("error", "Database connection failed")

    try:
        with connection.cursor() as cursor:
            cursor.execute(f"USE `{dataset.database_name}`")
            cursor.execute("SET SESSION TRANSACTION READ ONLY")
            cursor.execute("START TRANSACTION READ ONLY")
            cursor.execute(sql)

            description = cursor.description or []
            columns = [str(entry[0]) for entry in description]

            rows = cursor.fetchmany(MAX_ROWS + 1)
            if len(rows) > MAX_ROWS:
                connection.rollback()
                return [], [], f"Result contains too many rows (max {MAX_ROWS})"

            normalized_rows: list[list[Any]] = []
            for row in rows:
                if isinstance(row, dict):
                    normalized_rows.append([row.get(column) for column in columns])
                elif isinstance(row, (tuple, list)):
                    normalized_rows.append(list(row))
                else:
                    normalized_rows.append([row])

            connection.rollback()
            return columns, normalized_rows, None
    except Exception:
        connection.rollback()
        return [], [], "SQL execution failed"
    finally:
        connection.close()


def _canonical_row(row: list[Any]) -> str:
    return "|".join("NULL" if cell is None else str(cell).strip() for cell in row)


def _compare_result_sets(actual_rows: list[list[Any]], expected_rows: list[list[Any]]) -> tuple[bool, list[str], list[str]]:
    actual_set = sorted(_canonical_row(row) for row in actual_rows)
    expected_set = sorted(_canonical_row(row) for row in expected_rows)

    missing = [row for row in expected_set if row not in actual_set]
    extra = [row for row in actual_set if row not in expected_set]

    return len(missing) == 0 and len(extra) == 0, missing[:5], extra[:5]


def execute_sql_sandbox(payload: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    dataset_key = str(payload.get("dataset_key", "")).strip()
    candidate_sql = str(payload.get("candidate_sql", "")).strip()
    reference_sql = str(payload.get("reference_sql", "")).strip()

    registry = _dataset_registry()
    dataset = registry.get(dataset_key)
    if dataset is None:
        return None, "Unsupported dataset"

    valid_candidate, candidate_error = validate_sql_readonly(candidate_sql)
    if not valid_candidate:
        return None, candidate_error

    valid_reference, reference_error = validate_sql_readonly(reference_sql)
    if not valid_reference:
        return None, reference_error

    with _SANDBOX_LOCK:
        ready, prepare_error = _ensure_dataset(dataset)
    if not ready:
        return None, prepare_error

    actual_columns, actual_rows, actual_error = _run_select_query(dataset, candidate_sql)
    if actual_error:
        return None, actual_error

    expected_columns, expected_rows, expected_error = _run_select_query(dataset, reference_sql)
    if expected_error:
        return None, expected_error

    if len(actual_columns) != len(expected_columns):
        return {
            "ok": False,
            "score": 0,
            "actual": {
                "columns": actual_columns,
                "rows": actual_rows,
                "row_count": len(actual_rows),
            },
            "expected": {
                "columns": expected_columns,
                "rows": expected_rows,
                "row_count": len(expected_rows),
            },
            "feedback": {
                "message": "Die Anzahl der Ausgabespalten passt nicht zur Referenzloesung.",
                "missing_samples": [],
                "extra_samples": [],
            },
        }, None

    matched, missing_samples, extra_samples = _compare_result_sets(actual_rows, expected_rows)
    score = 100 if matched else max(0, 100 - ((len(missing_samples) + len(extra_samples)) * 10))

    return {
        "ok": matched,
        "score": score,
        "actual": {
            "columns": actual_columns,
            "rows": actual_rows,
            "row_count": len(actual_rows),
        },
        "expected": {
            "columns": expected_columns,
            "rows": expected_rows,
            "row_count": len(expected_rows),
        },
        "feedback": {
            "message": "Ergebnissatz passt zur Referenz." if matched else "Ergebnissatz weicht von der Referenz ab.",
            "missing_samples": missing_samples,
            "extra_samples": extra_samples,
        },
    }, None
