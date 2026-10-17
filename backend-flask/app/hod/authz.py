from functools import wraps

from flask import g, jsonify, request

from app.auth.utils import login_required


def hod_required(func):
    @wraps(func)
    @login_required
    def wrapper(*args, **kwargs):
        if g.current_user.role.code != "HOD":
            return jsonify({"error": {"message": "Forbidden"}}), 403
        return func(*args, **kwargs)
    return wrapper


def department_scope_for_user(user):
    return list(user.hod_departments)


def get_scoped_department_or_error(user, department_id=None):
    departments = department_scope_for_user(user)
    if not departments:
        return None, ("No department is assigned to this HOD", 403)
    if department_id is None:
        if len(departments) == 1:
            return departments[0], None
        return None, ("department_id is required for a multi-department HOD", 400)
    department = next((item for item in departments if item.id == department_id), None)
    if department is None:
        return None, ("Department not found", 404)
    return department, None
