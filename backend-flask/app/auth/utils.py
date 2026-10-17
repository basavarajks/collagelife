from functools import wraps

from flask import current_app, g, request
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

from app.extensions import db
from app.models import User


def _serializer() -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(current_app.config["SECRET_KEY"], salt="sdms-auth")


def generate_auth_token(user: User) -> str:
    payload = {
        "uid": user.id,
        "role": user.role.name,
    }
    return _serializer().dumps(payload)


def decode_auth_token(token: str) -> dict:
    serializer = _serializer()
    return serializer.loads(token, max_age=current_app.config["TOKEN_TTL_SECONDS"])


def auth_required(roles: list[str] | None = None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            header = request.headers.get("Authorization", "")
            if not header.startswith("Bearer "):
                return _error("Missing authorization header", 401)

            token = header.replace("Bearer ", "", 1).strip()
            if not token:
                return _error("Invalid token", 401)

            try:
                payload = decode_auth_token(token)
            except SignatureExpired:
                return _error("Token expired", 401)
            except BadSignature:
                return _error("Invalid token", 401)

            user = db.session.get(User, payload.get("uid"))
            if not user or not user.is_active:
                return _error("Unauthorized user", 403)

            if roles and user.role.name not in roles:
                return _error("Forbidden for this role", 403)

            g.current_user = user
            return func(*args, **kwargs)

        return wrapper

    return decorator


def _error(message: str, status_code: int):
    return {"error": {"message": message}}, status_code
