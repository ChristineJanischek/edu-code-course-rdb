import os

from flask import request

from .constants import API_VERSION
from .responses import api_error, create_trace_id


def configured_submission_api_key() -> str:
    return os.getenv("SUBMISSION_API_KEY", "")


def is_sensitive_submission_route(path: str) -> bool:
    return (
        path.startswith("/submissions")
        or path.startswith(f"/api/{API_VERSION}/submissions")
        or path.startswith("/sql-sandbox")
        or path.startswith(f"/api/{API_VERSION}/sql-sandbox")
    )


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


def apply_response_security_headers(response):
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


def handle_preflight_and_auth():
    if request.method == "OPTIONS":
        return "", 204

    if is_sensitive_submission_route(request.path):
        unauthorized_response = authorize_sensitive_submission_route()
        if unauthorized_response is not None:
            return unauthorized_response

    return None
