from flask import jsonify, request

from .assistant_routes import assistant_hint_route
from .constants import API_VERSION
from .curriculum_service import enrich_curriculum_index_documents, load_curriculum_document
from .db import mysql_status
from .responses import api_error, api_success, is_versioned_api_request
from .sql_sandbox_service import execute_sql_sandbox
from .storage import load_curriculum_index, load_json_db
from .submission_service import create_submission, list_submissions, normalize_submission_payload, submission_detail


def dual_response(payload, *, status_code: int = 200):
    if is_versioned_api_request():
        return api_success(payload, status_code=status_code)
    return jsonify(payload), status_code


def dual_error(versioned_code: str, message: str, *, status_code: int = 400, details: dict | None = None):
    if is_versioned_api_request():
        return api_error(versioned_code, message, status_code=status_code, details=details)
    return jsonify({"error": message if not details else details.get("error", message)}), status_code


def register_routes(app):
    app.add_url_rule(f"/api/{API_VERSION}/health", "health_v1", health)
    app.add_url_rule("/health", "health", health)

    app.add_url_rule(f"/api/{API_VERSION}/json-items", "json_items_v1", json_items)
    app.add_url_rule("/json-items", "json_items", json_items)

    app.add_url_rule(f"/api/{API_VERSION}/db-check", "db_check_v1", db_check)
    app.add_url_rule("/db-check", "db_check", db_check)

    app.add_url_rule(f"/api/{API_VERSION}/submissions", "create_submission_v1", create_submission_route, methods=["POST"])
    app.add_url_rule("/submissions", "create_submission", create_submission_route, methods=["POST"])

    app.add_url_rule(
        f"/api/{API_VERSION}/submissions/by-student/<student_id>",
        "list_submissions_v1",
        list_submissions_route,
    )
    app.add_url_rule("/submissions/by-student/<student_id>", "list_submissions", list_submissions_route)

    app.add_url_rule(f"/api/{API_VERSION}/submissions/<submission_uuid>", "submission_detail_v1", submission_detail_route)
    app.add_url_rule("/submissions/<submission_uuid>", "submission_detail", submission_detail_route)

    app.add_url_rule(f"/api/{API_VERSION}/curricula", "curricula_v1", curricula)
    app.add_url_rule("/curricula", "curricula", curricula)

    app.add_url_rule(f"/api/{API_VERSION}/curricula/<slug>", "curriculum_detail_v1", curriculum_detail)
    app.add_url_rule("/curricula/<slug>", "curriculum_detail", curriculum_detail)

    app.add_url_rule(
        f"/api/{API_VERSION}/sql-sandbox/execute",
        "sql_sandbox_execute_v1",
        sql_sandbox_execute_route,
        methods=["POST"],
    )
    app.add_url_rule("/sql-sandbox/execute", "sql_sandbox_execute", sql_sandbox_execute_route, methods=["POST"])

    app.add_url_rule(f"/api/{API_VERSION}/assistant/hint", "assistant_hint_v1", assistant_hint_entry, methods=["POST"])
    app.add_url_rule("/assistant/hint", "assistant_hint", assistant_hint_entry, methods=["POST"])


def health():
    payload = {
        "service": "python-api",
        "status": "ok",
        "mysql": mysql_status(),
        "json_loaded": "error" not in load_json_db(),
        "curriculum_loaded": "error" not in load_curriculum_index(),
    }
    return dual_response(payload)


def json_items():
    return dual_response(load_json_db())


def db_check():
    return dual_response(mysql_status())


def create_submission_route():
    payload = request.get_json(silent=True)
    normalized_payload, error_message = normalize_submission_payload(payload)
    if error_message:
        return dual_error("SUBMISSION_VALIDATION_FAILED", error_message, status_code=400)

    response_payload, db_error, error_code = create_submission(normalized_payload)
    if db_error is not None:
        return dual_error(error_code or "DATABASE_UNAVAILABLE", db_error.get("error", "Database connection failed"), status_code=503, details=db_error)
    if error_code == "SUBMISSION_SAVE_FAILED":
        return dual_error("SUBMISSION_SAVE_FAILED", "Submission could not be saved", status_code=500)

    return dual_response(response_payload, status_code=201)


def list_submissions_route(student_id):
    if not student_id or len(student_id) > 128:
        return dual_error("INVALID_STUDENT_ID", "Invalid student_id", status_code=400)

    learner_alias = request.args.get("learner_alias", type=str)
    task_id = request.args.get("task_id", type=str)
    limit = request.args.get("limit", default=20, type=int)
    limit = max(1, min(limit or 20, 100))

    response_payload, db_error, error_code = list_submissions(student_id, learner_alias, task_id, limit)
    if db_error is not None:
        return dual_error(error_code or "DATABASE_UNAVAILABLE", db_error.get("error", "Database connection failed"), status_code=503, details=db_error)
    if error_code == "SUBMISSIONS_LOAD_FAILED":
        return dual_error("SUBMISSIONS_LOAD_FAILED", "Submissions could not be loaded", status_code=500)

    return dual_response(response_payload)


def submission_detail_route(submission_uuid):
    response_payload, db_error, error_code = submission_detail(submission_uuid)
    if db_error is not None:
        return dual_error(error_code or "DATABASE_UNAVAILABLE", db_error.get("error", "Database connection failed"), status_code=503, details=db_error)
    if error_code == "SUBMISSION_NOT_FOUND":
        return dual_error("SUBMISSION_NOT_FOUND", "Submission not found", status_code=404)
    if error_code == "SUBMISSION_LOAD_FAILED":
        return dual_error("SUBMISSION_LOAD_FAILED", "Submission could not be loaded", status_code=500)

    return dual_response(response_payload)


def curricula():
    index_data = load_curriculum_index()
    if "error" in index_data:
        return dual_error("CURRICULUM_INDEX_NOT_FOUND", index_data["error"], status_code=404)

    return dual_response(enrich_curriculum_index_documents(index_data))


def curriculum_detail(slug):
    curriculum_doc = load_curriculum_document(slug)
    if "error" in curriculum_doc:
        return dual_error("CURRICULUM_NOT_FOUND", curriculum_doc["error"], status_code=404)

    return dual_response(curriculum_doc)


def sql_sandbox_execute_route():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return dual_error("SQL_SANDBOX_INVALID_PAYLOAD", "Invalid JSON payload", status_code=400)

    response_payload, error_message = execute_sql_sandbox(payload)
    if error_message:
        lowered = error_message.lower()
        if "unsupported dataset" in lowered or "empty" in lowered or "forbidden" in lowered or "only" in lowered:
            return dual_error("SQL_SANDBOX_VALIDATION_FAILED", error_message, status_code=400)

        if "too many rows" in lowered:
            return dual_error("SQL_SANDBOX_RESULT_TOO_LARGE", error_message, status_code=400)

        return dual_error("SQL_SANDBOX_EXECUTION_FAILED", error_message, status_code=500)

    return dual_response(response_payload)


def assistant_hint_entry():
    return assistant_hint_route(dual_response, dual_error)
