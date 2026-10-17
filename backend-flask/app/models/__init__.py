from app.models.academic import AcademicYear, Semester
from app.models.announcement import Announcement
from app.models.audit import AuditLog
from app.models.college import CollegeProfile
from app.models.department import Department
from app.models.permission import Permission
from app.models.role import Role
from app.models.token import AuthToken
from app.models.user import User

__all__ = ["AcademicYear", "Announcement", "AuditLog", "CollegeProfile", "Department", "Permission", "Role", "Semester", "AuthToken", "User"]
