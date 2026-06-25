import uuid

from flask import g, jsonify, request

from .constants import API_VERSION


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


def is_versioned_api_request(path: str | None = None) -> bool:
    request_path = path or request.path
    return request_path.startswith(f"/api/{API_VERSION}/")


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
