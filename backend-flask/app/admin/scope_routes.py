from flask import Blueprint, g, jsonify, request

from app.auth.utils import roles_required
from app.extensions import db
from app.models import Department, User

admin_scope_bp = Blueprint("admin_scope", __name__, url_prefix="/api/v1/admin")


@admin_scope_bp.put("/hod-assignments/<int:user_id>")
@roles_required("ADMIN_PRINCIPAL")
def assign_hod_departments(user_id):
    user = db.session.get(User, user_id)
    if not user or user.role.code != "HOD":
        return jsonify({"error": {"message": "HOD user not found"}}), 404
    payload = request.get_json(silent=True) or {}
    raw_ids = payload.get("department_ids")
    if not isinstance(raw_ids, list):
        return jsonify({"error": {"message": "department_ids must be an array"}}), 400
    try:
        ids = {int(value) for value in raw_ids}
    except (TypeError, ValueError):
        return jsonify({"error": {"message": "department_ids must contain integers"}}), 400
    departments = Department.query.filter(Department.id.in_(ids)).all() if ids else []
    if len(departments) != len(ids):
        return jsonify({"error": {"message": "One or more departments were not found"}}), 404
    user.hod_departments = departments
    db.session.commit()
    return jsonify({"data": {"user_id": user.id, "departments": [{"id": item.id, "code": item.code, "name": item.name} for item in departments]}})
