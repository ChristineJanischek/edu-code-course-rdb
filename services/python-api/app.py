import json
import os
import uuid
from pathlib import Path

import pymysql
from flask import Flask, g, jsonify, request

app = Flask(__name__)
API_VERSION = "v1"
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_REQUEST_BYTES", "262144"))

ALLOWED_SUBMISSION_KINDS = {
    "answer",
    "summary",
    "translation",
    "transcript",
    "note",
    "code",
}

SUBMISSION_SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS learning_submissions (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    submission_uuid CHAR(32) NOT NULL UNIQUE,
    learner_alias VARCHAR(80) NOT NULL,
    task_id VARCHAR(120) NOT NULL,
    response_kind VARCHAR(32) NOT NULL,
    response_text LONGTEXT NOT NULL,
    source_context VARCHAR(160) DEFAULT NULL,
    metadata_json LONGTEXT DEFAULT NULL,
    teacher_note LONGTEXT DEFAULT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'submitted',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_learning_submissions_learner_alias (learner_alias),
    INDEX idx_learning_submissions_task_id (task_id),
    INDEX idx_learning_submissions_created_at (created_at)
)
"""


def load_json_file(path_value: str) -> dict:
    json_path = Path(path_value)
    if not json_path.exists():
        return {"error": f"JSON-Datei nicht gefunden: {json_path}"}
    with json_path.open("r", encoding="utf-8") as f:
        return json.load(f)


def create_trace_id() -> str:
    trace_id = getattr(g, "trace_id", None)
    if not trace_id:
        trace_id = uuid.uuid4().hex
        g.trace_id = trace_id
    return trace_id


def api_metadata() -> dict:
    return {
        "api_version": API_VERSION,
        "trace_id": create_trace_id(),
    }


def api_success(data: dict | list | str | int | float | None, *, message: str | None = None, status_code: int = 200):
    payload = {"success": True, "data": data, "meta": api_metadata()}
    if message:
        payload["message"] = message
    response = jsonify(payload)
    response.status_code = status_code
    response.headers["X-Trace-Id"] = payload["meta"]["trace_id"]
    return response


def api_error(code: str, message: str, *, status_code: int = 400, details: dict | list | str | None = None):
    payload = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "meta": api_metadata(),
    }
    response = jsonify(payload)
    response.status_code = status_code
    response.headers["X-Trace-Id"] = payload["meta"]["trace_id"]
    return response


def is_versioned_api_request() -> bool:
    return request.path.startswith(f"/api/{API_VERSION}/")


def configured_submission_api_key() -> str:
    return os.getenv("SUBMISSION_API_KEY", "")


def is_sensitive_submission_route(path: str) -> bool:
    return path.startswith("/submissions") or path.startswith(f"/api/{API_VERSION}/submissions")


def authorize_sensitive_submission_route():
    expected_key = configured_submission_api_key()
    if not expected_key:
        return api_error("SUBMISSION_AUTH_NOT_CONFIGURED", "Submission API key is not configured", status_code=503)

    provided_key = request.headers.get("X-Internal-Api-Key", "")
    if provided_key != expected_key:
        return api_error("UNAUTHORIZED", "Missing or invalid submission API key", status_code=401)
    return None


def allowed_cors_origins() -> set[str]:
    configured = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:8080,http://127.0.0.1:8080")
    origins = {origin.strip() for origin in configured.split(",") if origin.strip()}

    codespace_name = os.getenv("CODESPACE_NAME")
    if codespace_name:
        for port in ("8080", "8000"):
            origins.add(f"https://{codespace_name}-{port}.githubpreview.dev")
            origins.add(f"https://{codespace_name}-{port}.app.github.dev")

    return origins


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


def internal_api_base_url() -> str:
    return os.getenv("PYTHON_API_INTERNAL_URL", os.getenv("PYTHON_API_URL", "http://python-api:8000"))


def ensure_submission_schema(connection):
    with connection.cursor() as cursor:
        cursor.execute(SUBMISSION_SCHEMA_SQL)


def serialize_submission_row(row: dict) -> dict:
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
    if status not in {"submitted", "draft", "reviewed", "published"}:
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


@app.after_request
def add_cors_headers(response):
    origin = request.headers.get("Origin")
    if origin and origin in allowed_cors_origins():
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Max-Age"] = "600"
        response.headers["Vary"] = "Origin"
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("Referrer-Policy", "no-referrer")
    response.headers.setdefault("X-Frame-Options", "SAMEORIGIN")
    response.headers.setdefault("Cache-Control", "no-store")
    response.headers.setdefault("X-Trace-Id", create_trace_id())
    return response


@app.before_request
def handle_cors_preflight():
    if request.method == "OPTIONS":
        return ("", 204)

    if is_sensitive_submission_route(request.path):
        unauthorized_response = authorize_sensitive_submission_route()
        if unauthorized_response is not None:
            return unauthorized_response


def load_json_db():
    return load_json_file(os.getenv("JSON_DB_PATH", "/app/data.json"))


def load_curriculum_index():
    return load_json_file(os.getenv("CURRICULUM_INDEX_PATH", "/app/generated/lehrplaene/index.json"))


def load_curriculum_document(slug: str):
    index_data = load_curriculum_index()
    if "error" in index_data:
        return index_data

    for document in index_data.get("documents", []):
        if document.get("slug") == slug:
            document_path = Path("/app") / document["document_json"]
            curriculum_doc = load_json_file(str(document_path))
            if "error" in curriculum_doc:
                return curriculum_doc
            curriculum_doc["recommendations"] = build_recommendations(curriculum_doc.get("tag_summary", {}))
            return curriculum_doc
    return {"error": f"Lehrplan nicht gefunden: {slug}"}


def build_recommendations(tag_summary: dict):
    recommendations = []

    if tag_summary.get("eerm", 0):
        recommendations.append(
            {
                "type": "learning-path",
                "title": "EERM vom Sachverhalt ableiten",
                "summary": "Starte mit fachlichen Objekten, Kardinalitaeten und Schluesselbeziehungen und sichere die Modellierung mit einem Begruendungsschritt ab.",
            }
        )
    if tag_summary.get("normalisierung", 0) or tag_summary.get("datenintegritaet", 0):
        recommendations.append(
            {
                "type": "exercise",
                "title": "3NF begruenden",
                "summary": "Ergänze Übungen, in denen Lernende Redundanzen erkennen, funktionale Abhängigkeiten benennen und ihr Zielmodell fachlich begründen.",
            }
        )
    if tag_summary.get("sql-select", 0) or tag_summary.get("sql-join", 0) or tag_summary.get("sql-group-by", 0):
        recommendations.append(
            {
                "type": "practice",
                "title": "SQL stufenweise trainieren",
                "summary": "Baue Aufgabenketten von einfacher SELECT-Abfrage über JOIN bis zu Aggregation und fachlicher Auswertung auf.",
            }
        )
    if tag_summary.get("begruendung", 0):
        recommendations.append(
            {
                "type": "feedback",
                "title": "Begruendung explizit einfordern",
                "summary": "Selbstkontrolle und Musterloesung sollen nicht nur Syntax, sondern auch fachliche Entscheidungen und Modellkritik sichtbar machen.",
            }
        )

    return recommendations


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


@app.get(f"/api/{API_VERSION}/health")
@app.get("/health")
def health():
    payload = {
        "service": "python-api",
        "status": "ok",
        "mysql": mysql_status(),
        "json_loaded": "error" not in load_json_db(),
        "curriculum_loaded": "error" not in load_curriculum_index(),
    }
    return api_success(payload) if is_versioned_api_request() else jsonify(payload)


@app.get(f"/api/{API_VERSION}/json-items")
@app.get("/json-items")
def json_items():
    payload = load_json_db()
    return api_success(payload) if is_versioned_api_request() else jsonify(payload)


@app.get(f"/api/{API_VERSION}/db-check")
@app.get("/db-check")
def db_check():
    payload = mysql_status()
    return api_success(payload) if is_versioned_api_request() else jsonify(payload)


@app.post(f"/api/{API_VERSION}/submissions")
@app.post("/submissions")
def create_submission():
    payload = request.get_json(silent=True)
    normalized_payload, error_message = normalize_submission_payload(payload)
    if error_message:
        if is_versioned_api_request():
            return api_error("SUBMISSION_VALIDATION_FAILED", error_message, status_code=400)
        return jsonify({"error": error_message}), 400

    connection, error_payload = db_connection()
    if connection is None:
        if is_versioned_api_request():
            return api_error("DATABASE_UNAVAILABLE", error_payload["error"], status_code=503, details=error_payload)
        return jsonify(error_payload), 503

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
        if is_versioned_api_request():
            return api_error("SUBMISSION_SAVE_FAILED", "Submission could not be saved", status_code=500)
        return jsonify({"error": "Submission could not be saved"}), 500
    finally:
        connection.close()

    response_payload = {
        "status": "created",
        "submission": {
            "submission_uuid": normalized_payload["submission_uuid"],
            "learner_alias": normalized_payload["learner_alias"],
            "task_id": normalized_payload["task_id"],
            "response_kind": normalized_payload["response_kind"],
            "status": normalized_payload["status"],
        },
    }
    return api_success(response_payload, status_code=201) if is_versioned_api_request() else jsonify(response_payload), 201


@app.get(f"/api/{API_VERSION}/submissions/by-student/<student_id>")
@app.get("/submissions/by-student/<student_id>")
def list_submissions(student_id):
    if not student_id or len(student_id) > 128:
        if is_versioned_api_request():
            return api_error("INVALID_STUDENT_ID", "Invalid student_id", status_code=400)
        return jsonify({"error": "Invalid student_id"}), 400

    learner_alias = request.args.get("learner_alias", type=str)
    task_id = request.args.get("task_id", type=str)
    limit = request.args.get("limit", default=20, type=int)
    limit = max(1, min(limit or 20, 100))

    if learner_alias is None:
        learner_alias = student_id

    connection, error_payload = db_connection()
    if connection is None:
        if is_versioned_api_request():
            return api_error("DATABASE_UNAVAILABLE", error_payload["error"], status_code=503, details=error_payload)
        return jsonify(error_payload), 503

    try:
        ensure_submission_schema(connection)
        query = ["SELECT * FROM learning_submissions WHERE 1=1"]
        parameters: list[object] = []

        if learner_alias:
            query.append("AND learner_alias = %s")
            parameters.append(learner_alias.strip())
        if task_id:
            query.append("AND task_id = %s")
            parameters.append(task_id.strip())

        query.append("ORDER BY created_at DESC LIMIT %s")
        parameters.append(limit)

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(" ".join(query), parameters)
            rows = cursor.fetchall()

        connection.commit()
        response_payload = {
            "submissions": [serialize_submission_row(row) for row in rows],
            "count": len(rows),
        }
        return api_success(response_payload) if is_versioned_api_request() else jsonify(response_payload)
    except Exception:
        connection.rollback()
        if is_versioned_api_request():
            return api_error("SUBMISSIONS_LOAD_FAILED", "Submissions could not be loaded", status_code=500)
        return jsonify({"error": "Submissions could not be loaded"}), 500
    finally:
        connection.close()


@app.get(f"/api/{API_VERSION}/submissions/<submission_uuid>")
@app.get("/submissions/<submission_uuid>")
def submission_detail(submission_uuid):
    connection, error_payload = db_connection()
    if connection is None:
        if is_versioned_api_request():
            return api_error("DATABASE_UNAVAILABLE", error_payload["error"], status_code=503, details=error_payload)
        return jsonify(error_payload), 503

    try:
        ensure_submission_schema(connection)
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(
                "SELECT * FROM learning_submissions WHERE submission_uuid = %s LIMIT 1",
                (submission_uuid,),
            )
            row = cursor.fetchone()

        if not row:
            if is_versioned_api_request():
                return api_error("SUBMISSION_NOT_FOUND", "Submission not found", status_code=404)
            return jsonify({"error": "Submission not found"}), 404

        connection.commit()
        response_payload = {"submission": serialize_submission_row(row)}
        return api_success(response_payload) if is_versioned_api_request() else jsonify(response_payload)
    except Exception:
        connection.rollback()
        if is_versioned_api_request():
            return api_error("SUBMISSION_LOAD_FAILED", "Submission could not be loaded", status_code=500)
        return jsonify({"error": "Submission could not be loaded"}), 500
    finally:
        connection.close()


@app.get(f"/api/{API_VERSION}/curricula")
@app.get("/curricula")
def curricula():
    index_data = load_curriculum_index()
    if "error" in index_data:
        if is_versioned_api_request():
            return api_error("CURRICULUM_INDEX_NOT_FOUND", index_data["error"], status_code=404)
        return jsonify(index_data), 404

    enriched_documents = []
    for document in index_data.get("documents", []):
        enriched_document = dict(document)
        enriched_document["recommendations"] = build_recommendations(document.get("tag_summary", {}))
        enriched_documents.append(enriched_document)

    payload = {"documents": enriched_documents}
    return api_success(payload) if is_versioned_api_request() else jsonify(payload)


@app.get(f"/api/{API_VERSION}/curricula/<slug>")
@app.get("/curricula/<slug>")
def curriculum_detail(slug):
    curriculum_doc = load_curriculum_document(slug)
    if "error" in curriculum_doc:
        if is_versioned_api_request():
            return api_error("CURRICULUM_NOT_FOUND", curriculum_doc["error"], status_code=404)
        return jsonify(curriculum_doc), 404
    return api_success(curriculum_doc) if is_versioned_api_request() else jsonify(curriculum_doc)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
