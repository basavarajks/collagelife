from flask import Blueprint, jsonify, g
from sqlalchemy import text

from app.auth.utils import login_required, permission_required, roles_required
from app.extensions import db

api_bp = Blueprint("api", __name__, url_prefix="/api/v1/api")


@api_bp.get("/health")
def health():
    try:
        db.session.execute(text("SELECT 1"))
        return jsonify({"status": "ok", "service": "sdms-phase2-auth", "database": "connected"})
    except Exception:
        db.session.rollback()
        return jsonify({"status": "degraded", "service": "sdms-phase2-auth", "database": "unavailable"}), 503


@api_bp.get("/protected")
@login_required
def protected():
    return jsonify({"data": {"message": "Protected access granted", "user": g.current_user.public_dict()}})


@api_bp.get("/principal-only")
@roles_required("ADMIN_PRINCIPAL")
def principal_only():
    return jsonify({"data": {"message": "Principal/Admin authorized endpoint"}})


@api_bp.get("/permission-example")
@permission_required("VIEW_COLLEGE_REPORTS")
def permission_example():
    return jsonify({"data": {"message": "Permission authorized"}})
