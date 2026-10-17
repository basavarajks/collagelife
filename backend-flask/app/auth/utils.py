import hashlib
import uuid
from datetime import datetime, timedelta, timezone
from functools import wraps

from flask import current_app, g, jsonify, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.extensions import db
from app.models import AuthToken, User


def _serializer():
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="sdms-auth")


def _hash_jti(jti):
    return hashlib.sha256(jti.encode("utf-8")).hexdigest()


def generate_auth_token(user):
    jti = uuid.uuid4().hex
    token = _serializer().dumps({"uid": user.id, "jti": jti})
    expires = datetime.now(timezone.utc).replace(tzinfo=None) + timedelta(seconds=current_app.config["TOKEN_TTL_SECONDS"])
    db.session.add(AuthToken(jti_hash=_hash_jti(jti), user_id=user.id, expires_at=expires))
    return token


def decode_auth_token(token):
    return _serializer().loads(token, max_age=current_app.config["TOKEN_TTL_SECONDS"])


def _token_from_request():
    header = request.headers.get("Authorization", "")
    if header.startswith("Bearer "):
        return header[7:].strip()
    return request.cookies.get(current_app.config["AUTH_TOKEN_COOKIE"])


def current_user_from_request():
    token = _token_from_request()
    if not token:
        return None, ("Missing authentication credentials", 401)
    try:
        payload = decode_auth_token(token)
    except SignatureExpired:
        return None, ("Authentication expired", 401)
    except BadSignature:
        return None, ("Invalid authentication credentials", 401)
    jti = payload.get("jti")
    record = AuthToken.query.filter_by(jti_hash=_hash_jti(jti or "")).first()
    user = db.session.get(User, payload.get("uid"))
    if not record or not record.is_valid or not user or not user.is_active:
        return None, ("Unauthorized", 401)
    return user, None


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user, error = current_user_from_request()
        if error:
            return jsonify({"error": {"message": error[0]}}), error[1]
        g.current_user = user
        return func(*args, **kwargs)
    return wrapper


def roles_required(*role_codes):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if g.current_user.role.code not in role_codes:
                return jsonify({"error": {"message": "Forbidden"}}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator


def permission_required(permission_code):
    def decorator(func):
        @wraps(func)
        @login_required
        def wrapper(*args, **kwargs):
            if not g.current_user.role.has_permission(permission_code):
                return jsonify({"error": {"message": "Forbidden"}}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator
