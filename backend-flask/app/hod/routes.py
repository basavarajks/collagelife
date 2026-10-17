from datetime import datetime, timezone

from flask import Blueprint, g, jsonify, request
from sqlalchemy import func, or_

from app.extensions import db
from app.hod.authz import get_scoped_department_or_error, hod_required
from app.models import AcademicYear, Announcement, AuditLog, Department, Role, User

hod_bp = Blueprint("hod", __name__, url_prefix="/api/v1/hod")


def error(message, status=400):
    return jsonify({"error": {"message": message}}), status


def resolve_department():
    raw_id = request.args.get("department_id") or request.view_args.get("department_id")
    try:
        department_id = int(raw_id) if raw_id is not None else None
    except ValueError:
        return None, ("department_id must be an integer", 400)
    return get_scoped_department_or_error(g.current_user, department_id)


def department_dict(item):
    return {
        "id": item.id,
        "code": item.code,
        "name": item.name,
        "description": item.description,
        "is_active": item.is_active,
        "head_user_id": item.head_user_id,
        "head_name": item.head.full_name if item.head else None,
    }


def announcement_dict(item):
    return {
        "id": item.id,
        "title": item.title,
        "message": item.message,
        "status": item.status,
        "audience": item.audience,
        "department_id": item.department_id,
        "publish_at": item.publish_at.isoformat() if item.publish_at else None,
        "expires_at": item.expires_at.isoformat() if item.expires_at else None,
        "created_at": item.created_at.isoformat(),
    }


@hod_bp.get("/dashboard")
@hod_required
def dashboard():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    faculty_role = Role.query.filter_by(code="FACULTY").first()
    faculty_count = 0
    if faculty_role:
        faculty_count = User.query.filter(User.role_id == faculty_role.id, User.is_active.is_(True)).filter(
            User.id.in_(db.select(db.literal(-1)))
        ).count()
    announcement_count = Announcement.query.filter_by(department_id=department.id, status="PUBLISHED").count()
    current_year = AcademicYear.query.filter_by(is_current=True).first()
    return jsonify({"data": {
        "department": department_dict(department),
        "students": 0,
        "faculty": faculty_count,
        "subjects": 0,
        "current_academic_year": current_year.name if current_year else None,
        "announcements": announcement_count,
        "recent_activity": [{"event_type": item.event_type, "created_at": item.created_at.isoformat()} for item in AuditLog.query.filter(AuditLog.metadata_json.is_not(None)).order_by(AuditLog.created_at.desc()).limit(10)],
        "availability": {"students": False, "faculty": False, "subjects": False, "assignments": False},
    }})


@hod_bp.get("/department")
@hod_required
def department_profile():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    return jsonify({"data": {"department": department_dict(department)}})


@hod_bp.get("/faculty")
@hod_required
def faculty_overview():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    return jsonify({"data": {"items": [], "page": 1, "pages": 0, "total": 0, "available": False, "message": "Faculty department relationships are not implemented yet."}})


@hod_bp.get("/students")
@hod_required
def student_overview():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    return jsonify({"data": {"items": [], "page": 1, "pages": 0, "total": 0, "available": False, "message": "Student records are not implemented yet."}})


@hod_bp.get("/academic-structure")
@hod_required
def academic_structure():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    years = AcademicYear.query.order_by(AcademicYear.start_date.desc()).all()
    return jsonify({"data": {"department": department_dict(department), "items": [{"id": year.id, "name": year.name, "start_date": year.start_date.isoformat(), "end_date": year.end_date.isoformat(), "status": year.status, "is_current": year.is_current, "semesters": [{"id": semester.id, "number": semester.number, "name": semester.name, "start_date": semester.start_date.isoformat(), "end_date": semester.end_date.isoformat(), "status": semester.status} for semester in year.semesters]} for year in years]}})


@hod_bp.get("/faculty-assignments")
@hod_required
def assignments():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    return jsonify({"data": {"items": [], "available": False, "message": "Faculty assignment records are planned for a later phase."}})


@hod_bp.get("/announcements")
@hod_required
def announcements():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    items = Announcement.query.filter(or_(Announcement.department_id == department.id, Announcement.department_id.is_(None))).filter(Announcement.status == "PUBLISHED").order_by(Announcement.created_at.desc()).all()
    return jsonify({"data": {"items": [announcement_dict(item) for item in items]}})


@hod_bp.post("/announcements")
@hod_required
def create_announcement():
    payload = request.get_json(silent=True) or {}
    department_id = payload.get("department_id")
    try:
        department_id = int(department_id) if department_id is not None else None
    except (TypeError, ValueError):
        return error("department_id must be an integer")
    department, scope_error = get_scoped_department_or_error(g.current_user, department_id)
    if scope_error:
        return error(*scope_error)
    title = (payload.get("title") or "").strip()
    message = (payload.get("message") or "").strip()
    if not title or not message or len(title) > 200:
        return error("A title and message are required; title must be 200 characters or fewer")
    item = Announcement(title=title, message=message, audience=(payload.get("audience") or "ALL").strip(), status="DRAFT", created_by=g.current_user.id, department_id=department.id)
    db.session.add(item)
    db.session.add(AuditLog(event_type="HOD_ANNOUNCEMENT_CREATED", user_id=g.current_user.id, metadata_json={"department_id": department.id, "announcement_id": item.id}))
    db.session.commit()
    return jsonify({"data": {"announcement": announcement_dict(item)}}), 201


@hod_bp.put("/announcements/<int:announcement_id>")
@hod_required
def update_announcement(announcement_id):
    item = db.session.get(Announcement, announcement_id)
    if not item:
        return error("Announcement not found", 404)
    if item.department_id is None:
        return error("College-wide announcements are managed by Admin/Principal", 403)
    department, scope_error = get_scoped_department_or_error(g.current_user, item.department_id)
    if scope_error:
        return error(*scope_error)
    payload = request.get_json(silent=True) or {}
    if "status" in payload and payload["status"] not in {"DRAFT", "PUBLISHED", "ARCHIVED"}:
        return error("Invalid announcement status")
    for field in ("title", "message", "audience", "status"):
        if field in payload:
            value = payload[field].strip() if isinstance(payload[field], str) else payload[field]
            if field in {"title", "message"} and not value:
                return error(f"{field} cannot be empty")
            setattr(item, field, value)
    if item.status == "PUBLISHED" and not item.publish_at:
        item.publish_at = datetime.now(timezone.utc)
    db.session.add(AuditLog(event_type="HOD_ANNOUNCEMENT_UPDATED", user_id=g.current_user.id, metadata_json={"department_id": department.id, "announcement_id": item.id}))
    db.session.commit()
    return jsonify({"data": {"announcement": announcement_dict(item)}})


@hod_bp.get("/reports")
@hod_required
def reports():
    department, scope_error = resolve_department()
    if scope_error:
        return error(*scope_error)
    return jsonify({"data": {"department": department_dict(department), "student_count": 0, "faculty_count": 0, "announcement_count": Announcement.query.filter_by(department_id=department.id).count(), "available": {"students": False, "faculty": False, "assignments": False}, "message": "Student, faculty, and assignment reports will be enabled when those modules are implemented."}})
