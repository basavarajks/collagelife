from flask import Blueprint, current_app, jsonify, request

from app.extensions import db
from app.models import User

from .utils import generate_auth_token


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user_id = (payload.get("user_id") or "").strip()
    password = payload.get("password") or ""

    if not user_id or not password:
        return _error("user_id and password are required", 400)

    if not current_app.config.get("DATABASE_CONFIGURED"):
        return _error(
            "Database credentials are not configured. Set DATABASE_URL or DB_USER/DB_PASSWORD for MySQL/MariaDB.",
            503,
        )

    try:
        user = User.query.filter_by(user_id=user_id).first()
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Database error during login for user_id=%s", user_id)
        return _error("Database connection/configuration error.", 503)

    if not user or not user.check_password(password):
        return _error("Invalid credentials", 401)

    if not user.is_active:
        return _error("Account is inactive. Contact administrator.", 403)

    token = generate_auth_token(user)
    return jsonify(
        {
            "data": {
                "token": token,
                "user": {
                    "id": user.id,
                    "user_id": user.user_id,
                    "full_name": user.full_name,
                    "role": user.role.name,
                },
            }
        }
    )


@auth_bp.post("/forgot-password")
def forgot_password():
    return _error(
        "Forgot-password is not configured in Phase 1. No email/message delivery is currently implemented.",
        501,
    )


def _error(message: str, status_code: int):
    return jsonify({"error": {"message": message}}), status_code
