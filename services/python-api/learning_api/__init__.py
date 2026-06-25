from flask import Flask

from .constants import MAX_REQUEST_BYTES
from .routes import register_routes
from .security import apply_response_security_headers, handle_preflight_and_auth


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["MAX_CONTENT_LENGTH"] = MAX_REQUEST_BYTES

    app.after_request(apply_response_security_headers)
    app.before_request(handle_preflight_and_auth)
    register_routes(app)

    return app
