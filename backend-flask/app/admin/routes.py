from datetime import date, datetime, timezone

from flask import Blueprint, g, jsonify, request
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.auth.utils import roles_required
from app.extensions import db
from app.models import AcademicYear, Announcement, AuditLog, CollegeProfile, Department, Role, Semester, User

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


def error(message, status=400):
    return jsonify({"error": {"message": message}}), status


def parse_date(value, field):
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field} must use YYYY-MM-DD format")


def department_dict(item):
    return {"id": item.id, "code": item.code, "name": item.name, "description": item.description, "is_active": item.is_active, "head_user_id": item.head_user_id, "created_at": item.created_at.isoformat()}


@admin_bp.get("/dashboard")
@roles_required("ADMIN_PRINCIPAL")
def dashboard():
    role_counts = db.session.query(Role.code, func.count(User.id)).outerjoin(User).group_by(Role.code).all()
    counts = {code: count for code, count in role_counts}
    return jsonify({"data": {"students": counts.get("STUDENT", 0), "faculty": counts.get("FACULTY", 0), "office_staff": counts.get("OFFICE_STAFF", 0), "library_staff": counts.get("LIBRARY_STAFF", 0), "departments": Department.query.filter_by(is_active=True).count(), "active_academic_year": AcademicYear.query.filter_by(is_current=True).first().name if AcademicYear.query.filter_by(is_current=True).first() else None, "recent_audit": [{"event_type": item.event_type, "created_at": item.created_at.isoformat(), "user_id": item.user_id} for item in AuditLog.query.order_by(AuditLog.created_at.desc()).limit(8)]}})


@admin_bp.get("/profile")
@roles_required("ADMIN_PRINCIPAL")
def get_profile():
    profile = CollegeProfile.query.first()
    return jsonify({"data": {"profile": profile_dict(profile) if profile else None}})


@admin_bp.put("/profile")
@roles_required("ADMIN_PRINCIPAL")
def update_profile():
    payload = request.get_json(silent=True) or {}
    name = (payload.get("name") or "").strip()
    if not name or len(name) > 200:
        return error("College name is required and must be 200 characters or fewer")
    profile = CollegeProfile.query.first() or CollegeProfile(name=name)
    profile.name = name
    for field in ("code", "logo_path", "address", "contact_email", "contact_phone", "website", "description"):
        if field in payload:
            value = payload[field]
            setattr(profile, field, value.strip() if isinstance(value, str) else value)
    if payload.get("established_year") not in (None, ""):
        try:
            profile.established_year = int(payload["established_year"])
        except (TypeError, ValueError):
            return error("Established year must be a number")
    db.session.add(profile)
    db.session.add(AuditLog(event_type="COLLEGE_PROFILE_UPDATED", user_id=g.current_user.id, metadata_json={"profile_id": profile.id}))
    db.session.commit()
    return jsonify({"data": {"profile": profile_dict(profile)}})


def profile_dict(profile):
    return {"id": profile.id, "name": profile.name, "code": profile.code, "logo_path": profile.logo_path, "address": profile.address, "contact_email": profile.contact_email, "contact_phone": profile.contact_phone, "website": profile.website, "description": profile.description, "established_year": profile.established_year}


@admin_bp.get("/departments")
@roles_required("ADMIN_PRINCIPAL")
def departments():
    query = Department.query
    search = (request.args.get("search") or "").strip()
    if search:
        query = query.filter(db.or_(Department.name.ilike(f"%{search}%"), Department.code.ilike(f"%{search}%")))
    status = request.args.get("status")
    if status in {"active", "inactive"}:
        query = query.filter_by(is_active=status == "active")
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 10, type=int), 1), 100)
    result = query.order_by(Department.name.asc()).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({"data": {"items": [department_dict(item) for item in result.items], "page": page, "per_page": per_page, "pages": result.pages, "total": result.total}})


@admin_bp.post("/departments")
@roles_required("ADMIN_PRINCIPAL")
def create_department():
    payload = request.get_json(silent=True) or {}
    code, name = (payload.get("code") or "").strip().upper(), (payload.get("name") or "").strip()
    if not code or not name:
        return error("Department code and name are required")
    if Department.query.filter_by(code=code).first():
        return error("Department code already exists", 409)
    item = Department(code=code, name=name, description=(payload.get("description") or "").strip() or None)
    db.session.add(item)
    db.session.add(AuditLog(event_type="DEPARTMENT_CREATED", user_id=g.current_user.id, metadata_json={"code": code}))
    db.session.commit()
    return jsonify({"data": {"department": department_dict(item)}}), 201


@admin_bp.patch("/departments/<int:department_id>")
@roles_required("ADMIN_PRINCIPAL")
def update_department(department_id):
    item = db.session.get(Department, department_id)
    if not item:
        return error("Department not found", 404)
    payload = request.get_json(silent=True) or {}
    if "name" in payload and not (payload["name"] or "").strip():
        return error("Department name cannot be empty")
    if "code" in payload:
        code = payload["code"].strip().upper()
        duplicate = Department.query.filter(Department.code == code, Department.id != item.id).first()
        if duplicate:
            return error("Department code already exists", 409)
        item.code = code
    for field in ("name", "description"):
        if field in payload:
            setattr(item, field, payload[field].strip() if isinstance(payload[field], str) else payload[field])
    if "is_active" in payload:
        item.is_active = bool(payload["is_active"])
    db.session.add(AuditLog(event_type="DEPARTMENT_UPDATED", user_id=g.current_user.id, metadata_json={"department_id": item.id}))
    db.session.commit()
    return jsonify({"data": {"department": department_dict(item)}})


@admin_bp.get("/academic-years")
@roles_required("ADMIN_PRINCIPAL")
def academic_years():
    items = AcademicYear.query.order_by(AcademicYear.start_date.desc()).all()
    return jsonify({"data": {"items": [{"id": x.id, "name": x.name, "start_date": x.start_date.isoformat(), "end_date": x.end_date.isoformat(), "status": x.status, "is_current": x.is_current, "semesters": [{"id": s.id, "number": s.number, "name": s.name, "start_date": s.start_date.isoformat(), "end_date": s.end_date.isoformat(), "status": s.status} for s in x.semesters]} for x in items]}})


@admin_bp.post("/academic-years")
@roles_required("ADMIN_PRINCIPAL")
def create_academic_year():
    payload = request.get_json(silent=True) or {}
    try:
        start, end = parse_date(payload.get("start_date"), "start_date"), parse_date(payload.get("end_date"), "end_date")
    except ValueError as exc:
        return error(str(exc))
    if end <= start:
        return error("end_date must be after start_date")
    if not (payload.get("name") or "").strip():
        return error("Academic year name is required")
    if payload.get("is_current"):
        AcademicYear.query.update({"is_current": False})
    item = AcademicYear(name=payload["name"].strip(), start_date=start, end_date=end, status=payload.get("status", "PLANNED"), is_current=bool(payload.get("is_current")))
    db.session.add(item)
    db.session.add(AuditLog(event_type="ACADEMIC_YEAR_CREATED", user_id=g.current_user.id, metadata_json={"name": item.name}))
    db.session.commit()
    return jsonify({"data": {"id": item.id, "name": item.name}}), 201


@admin_bp.get("/announcements")
@roles_required("ADMIN_PRINCIPAL")
def announcements():
    items = Announcement.query.order_by(Announcement.created_at.desc()).all()
    return jsonify({"data": {"items": [{"id": x.id, "title": x.title, "message": x.message, "status": x.status, "audience": x.audience, "publish_at": x.publish_at.isoformat() if x.publish_at else None, "expires_at": x.expires_at.isoformat() if x.expires_at else None} for x in items]}})


@admin_bp.post("/announcements")
@roles_required("ADMIN_PRINCIPAL")
def create_announcement():
    payload = request.get_json(silent=True) or {}
    title, message = (payload.get("title") or "").strip(), (payload.get("message") or "").strip()
    if not title or not message:
        return error("Title and message are required")
    item = Announcement(title=title, message=message, audience=payload.get("audience", "ALL"), status="DRAFT", created_by=g.current_user.id)
    db.session.add(item)
    db.session.add(AuditLog(event_type="ANNOUNCEMENT_CREATED", user_id=g.current_user.id, metadata_json={"title": title}))
    db.session.commit()
    return jsonify({"data": {"id": item.id, "title": item.title, "status": item.status}}), 201


@admin_bp.patch("/announcements/<int:announcement_id>")
@roles_required("ADMIN_PRINCIPAL")
def update_announcement(announcement_id):
    item = db.session.get(Announcement, announcement_id)
    if not item:
        return error("Announcement not found", 404)
    payload = request.get_json(silent=True) or {}
    if "status" in payload and payload["status"] not in {"DRAFT", "PUBLISHED", "ARCHIVED"}:
        return error("Invalid announcement status")
    for field in ("title", "message", "audience", "status"):
        if field in payload:
            setattr(item, field, payload[field].strip() if isinstance(payload[field], str) else payload[field])
    if item.status == "PUBLISHED" and not item.publish_at:
        item.publish_at = datetime.now(timezone.utc)
    db.session.add(AuditLog(event_type="ANNOUNCEMENT_UPDATED", user_id=g.current_user.id, metadata_json={"announcement_id": item.id, "status": item.status}))
    db.session.commit()
    return jsonify({"data": {"id": item.id, "status": item.status}})


@admin_bp.get("/audit-logs")
@roles_required("ADMIN_PRINCIPAL")
def audit_logs():
    page = max(request.args.get("page", 1, type=int), 1)
    result = AuditLog.query.order_by(AuditLog.created_at.desc()).paginate(page=page, per_page=25, error_out=False)
    return jsonify({"data": {"items": [{"id": x.id, "event_type": x.event_type, "user_id": x.user_id, "metadata": x.metadata_json, "created_at": x.created_at.isoformat()} for x in result.items], "page": page, "pages": result.pages, "total": result.total}})
