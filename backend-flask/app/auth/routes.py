from datetime import datetime, timezone

from flask import Blueprint, current_app, g, jsonify, request, make_response
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import AuditLog, AuthToken, User

from .utils import generate_auth_token, login_required, current_user_from_request, _hash_jti, _token_from_request


auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


def _error(message, status_code):
    return jsonify({"error": {"message": message}}), status_code


def _audit(event_type, user_id=None, metadata=None):
    db.session.add(AuditLog(event_type=event_type, user_id=user_id, metadata_json=metadata))


def _user_response(user):
    return jsonify({"data": {"user": user.public_dict()}})


@auth_bp.post("/login")
def login():
    payload = request.get_json(silent=True) or {}
    user_id = (payload.get("user_id") or "").strip()
    password = payload.get("password") or ""
    if not user_id or not password:
        return _error("user_id and password are required", 400)
    if not current_app.config.get("DATABASE_CONFIGURED"):
        return _error("Database is not configured. Set DATABASE_URL or DB_USER/DB_PASSWORD.", 503)
    try:
        user = User.query.filter_by(user_id=user_id).first()
        if not user or not user.check_password(password):
            _audit("LOGIN_FAILED", user.id if user else None)
            db.session.commit()
            return _error("Invalid credentials", 401)
        if not user.is_active:
            _audit("LOGIN_FAILED_INACTIVE", user.id)
            db.session.commit()
            return _error("Invalid credentials", 401)
        user.last_login_at = datetime.now(timezone.utc)
        token = generate_auth_token(user)
        _audit("LOGIN_SUCCESS", user.id)
        db.session.commit()
        response = make_response(jsonify({"data": {"token": token, "user": user.public_dict()}}))
        if current_app.config.get("AUTH_USE_COOKIE", False):
            response.set_cookie(current_app.config["AUTH_TOKEN_COOKIE"], token, httponly=True, secure=current_app.config["AUTH_COOKIE_SECURE"], samesite=current_app.config["AUTH_COOKIE_SAMESITE"], max_age=current_app.config["TOKEN_TTL_SECONDS"])
        return response
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Database error during login")
        return _error("Database connection/configuration error.", 503)


@auth_bp.post("/logout")
@login_required
def logout():
    token = _token_from_request()
    try:
        payload = current_user_from_request()[0]
        if token:
            from .utils import decode_auth_token
            decoded = decode_auth_token(token)
            record = AuthToken.query.filter_by(jti_hash=_hash_jti(decoded.get("jti", ""))).first()
            if record:
                record.revoked_at = datetime.now(timezone.utc)
        _audit("LOGOUT", payload.id)
        db.session.commit()
        response = make_response(jsonify({"data": {"message": "Logged out"}}))
        response.delete_cookie(current_app.config["AUTH_TOKEN_COOKIE"])
        return response
    except Exception:
        db.session.rollback()
        return _error("Unable to complete logout", 503)


@auth_bp.get("/me")
@login_required
def me():
    return _user_response(g.current_user)


@auth_bp.post("/change-password")
@login_required
def change_password():
    payload = request.get_json(silent=True) or {}
    current = payload.get("current_password") or ""
    new = payload.get("new_password") or ""
    if len(new) < 8:
        return _error("New password must contain at least 8 characters", 400)
    if not g.current_user.check_password(current):
        return _error("Current password is incorrect", 400)
    g.current_user.set_password(new)
    _audit("PASSWORD_CHANGED", g.current_user.id)
    db.session.commit()
    return jsonify({"data": {"message": "Password changed successfully"}})


@auth_bp.post("/forgot-password")
def forgot_password():
    return _error("Password-reset delivery is not configured. Contact an administrator.", 501)
