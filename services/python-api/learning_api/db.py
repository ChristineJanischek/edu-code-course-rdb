import os

import pymysql

from .constants import SUBMISSION_SCHEMA_SQL


def db_connection():
    host = os.getenv("MYSQL_HOST", "mysql")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    user = os.getenv("MYSQL_USER", "appuser")
    password = os.getenv("MYSQL_PASSWORD", "")
    database = os.getenv("MYSQL_DATABASE", "appdb")

    if not password:
        return None, {"ok": False, "error": "MYSQL_PASSWORD not configured"}

    try:
        connection = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            connect_timeout=5,
            charset="utf8mb4",
            autocommit=False,
        )
    except Exception:
        return None, {"ok": False, "error": "Database connection failed"}

    return connection, None


def ensure_submission_schema(connection):
    with connection.cursor() as cursor:
        cursor.execute(SUBMISSION_SCHEMA_SQL)


def serialize_submission_row(row: dict) -> dict:
    import json

    metadata = row.get("metadata_json")
    parsed_metadata = None
    if isinstance(metadata, str) and metadata.strip():
        try:
            parsed_metadata = json.loads(metadata)
        except json.JSONDecodeError:
            parsed_metadata = metadata

    created_at = row.get("created_at")
    updated_at = row.get("updated_at")

    return {
        "submission_uuid": row.get("submission_uuid"),
        "learner_alias": row.get("learner_alias"),
        "task_id": row.get("task_id"),
        "response_kind": row.get("response_kind"),
        "response_text": row.get("response_text"),
        "source_context": row.get("source_context"),
        "metadata": parsed_metadata,
        "teacher_note": row.get("teacher_note"),
        "status": row.get("status"),
        "created_at": created_at.isoformat(sep=" ", timespec="seconds") if hasattr(created_at, "isoformat") else created_at,
        "updated_at": updated_at.isoformat(sep=" ", timespec="seconds") if hasattr(updated_at, "isoformat") else updated_at,
    }


def mysql_status():
    connection, error_payload = db_connection()
    if connection is None:
        return error_payload

    try:
        ensure_submission_schema(connection)
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) AS cnt FROM demo_items")
            demo_row = cursor.fetchone()
            if isinstance(demo_row, dict):
                demo_count = demo_row.get("cnt", 0)
            elif isinstance(demo_row, (list, tuple)) and demo_row:
                demo_count = demo_row[0]
            else:
                demo_count = 0

            cursor.execute("SELECT COUNT(*) AS cnt FROM learning_submissions")
            submission_row = cursor.fetchone()
            if isinstance(submission_row, dict):
                submission_count = submission_row.get("cnt", 0)
            elif isinstance(submission_row, (list, tuple)) and submission_row:
                submission_count = submission_row[0]
            else:
                submission_count = 0

        connection.commit()
        return {"ok": True, "demo_items": demo_count, "submissions": submission_count}
    except Exception:
        return {"ok": False, "error": "Database connection failed"}
    finally:
        connection.close()
