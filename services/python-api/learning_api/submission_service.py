import json
import uuid

import pymysql

from .constants import ALLOWED_SUBMISSION_KINDS, ALLOWED_SUBMISSION_STATUS
from .db import db_connection, ensure_submission_schema, serialize_submission_row


def normalize_submission_payload(payload: object) -> tuple[dict | None, str | None]:
    if not isinstance(payload, dict):
        return None, "JSON body must be an object"

    def first_present(*field_names: str):
        for field_name in field_names:
            if field_name in payload and payload[field_name] is not None:
                return payload[field_name]
        return None

    def require_text(field_name: str, max_length: int) -> str:
        value = first_present(field_name)
        if not isinstance(value, str):
            raise ValueError(f"Field '{field_name}' must be a string")
        normalized = value.strip()
        if not normalized:
            raise ValueError(f"Field '{field_name}' must not be empty")
        if len(normalized) > max_length:
            raise ValueError(f"Field '{field_name}' is too long")
        return normalized

    try:
        learner_alias = require_text("learner_alias", 80) if first_present("learner_alias", "student_id") is not None else require_text("student_id", 80)
        task_id = require_text("task_id", 120)
        response_text_value = first_present("response_text", "content")
        response_text = require_text("response_text", 12000) if response_text_value is not None else require_text("content", 12000)
        response_kind_value = first_present("response_kind", "content_type")
        response_kind = require_text("response_kind", 32).lower() if response_kind_value is not None else require_text("content_type", 32).lower()
    except ValueError as exc:
        return None, str(exc)

    if response_kind not in ALLOWED_SUBMISSION_KINDS:
        return None, f"Unsupported response_kind: {response_kind}"

    source_context = first_present("source_context", "source")
    if source_context is not None:
        if not isinstance(source_context, str):
            return None, "Field 'source_context' must be a string"
        source_context = source_context.strip() or None
        if source_context and len(source_context) > 160:
            return None, "Field 'source_context' is too long"

    status = payload.get("status", "submitted")
    if not isinstance(status, str):
        return None, "Field 'status' must be a string"
    status = status.strip().lower() or "submitted"
    if status not in ALLOWED_SUBMISSION_STATUS:
        return None, f"Unsupported status: {status}"

    metadata = first_present("metadata")
    metadata_json = None
    if metadata is not None:
        try:
            metadata_json = json.dumps(metadata, ensure_ascii=False)
        except TypeError:
            return None, "Field 'metadata' must be JSON serializable"

    teacher_note = first_present("teacher_note")
    if teacher_note is not None:
        if not isinstance(teacher_note, str):
            return None, "Field 'teacher_note' must be a string"
        teacher_note = teacher_note.strip() or None
        if teacher_note and len(teacher_note) > 12000:
            return None, "Field 'teacher_note' is too long"

    return {
        "submission_uuid": uuid.uuid4().hex,
        "learner_alias": learner_alias,
        "task_id": task_id,
        "response_kind": response_kind,
        "response_text": response_text,
        "source_context": source_context,
        "metadata_json": metadata_json,
        "teacher_note": teacher_note,
        "status": status,
    }, None


def create_submission(normalized_payload: dict) -> tuple[dict | None, dict | None, str | None]:
    connection, error_payload = db_connection()
    if connection is None:
        return None, error_payload, "DATABASE_UNAVAILABLE"

    try:
        ensure_submission_schema(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO learning_submissions (
                    submission_uuid,
                    learner_alias,
                    task_id,
                    response_kind,
                    response_text,
                    source_context,
                    metadata_json,
                    teacher_note,
                    status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    normalized_payload["submission_uuid"],
                    normalized_payload["learner_alias"],
                    normalized_payload["task_id"],
                    normalized_payload["response_kind"],
                    normalized_payload["response_text"],
                    normalized_payload["source_context"],
                    normalized_payload["metadata_json"],
                    normalized_payload["teacher_note"],
                    normalized_payload["status"],
                ),
            )
        connection.commit()
    except Exception:
        connection.rollback()
        return None, None, "SUBMISSION_SAVE_FAILED"
    finally:
        connection.close()

    return {
        "status": "created",
        "submission": {
            "submission_uuid": normalized_payload["submission_uuid"],
            "learner_alias": normalized_payload["learner_alias"],
            "task_id": normalized_payload["task_id"],
            "response_kind": normalized_payload["response_kind"],
            "status": normalized_payload["status"],
        },
    }, None, None


def list_submissions(student_id: str, learner_alias: str | None, task_id: str | None, limit: int) -> tuple[dict | None, dict | None, str | None]:
    connection, error_payload = db_connection()
    if connection is None:
        return None, error_payload, "DATABASE_UNAVAILABLE"

    try:
        ensure_submission_schema(connection)
        query = ["SELECT * FROM learning_submissions WHERE 1=1"]
        parameters: list[object] = []

        alias = learner_alias if learner_alias is not None else student_id
        if alias:
            query.append("AND learner_alias = %s")
            parameters.append(alias.strip())
        if task_id:
            query.append("AND task_id = %s")
            parameters.append(task_id.strip())

        query.append("ORDER BY created_at DESC LIMIT %s")
        parameters.append(limit)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(" ".join(query), parameters)
            rows = cursor.fetchall()

        connection.commit()
        return {
            "submissions": [serialize_submission_row(row) for row in rows],
            "count": len(rows),
        }, None, None
    except Exception:
        connection.rollback()
        return None, None, "SUBMISSIONS_LOAD_FAILED"
    finally:
        connection.close()


def submission_detail(submission_uuid: str) -> tuple[dict | None, dict | None, str | None]:
    connection, error_payload = db_connection()
    if connection is None:
        return None, error_payload, "DATABASE_UNAVAILABLE"

    try:
        ensure_submission_schema(connection)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM learning_submissions WHERE submission_uuid = %s LIMIT 1",
                (submission_uuid,),
            )
            row = cursor.fetchone()

        if not row:
            return None, None, "SUBMISSION_NOT_FOUND"

        connection.commit()
        return {"submission": serialize_submission_row(row)}, None, None
    except Exception:
        connection.rollback()
        return None, None, "SUBMISSION_LOAD_FAILED"
    finally:
        connection.close()
