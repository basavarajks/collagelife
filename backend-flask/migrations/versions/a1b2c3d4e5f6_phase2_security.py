import uuid
from alembic import op
import sqlalchemy as sa

revision = "a1b2c3d4e5f6"
down_revision = "7fb525992ec8"
branch_labels = None
depends_on = None

ROLE_SEEDS = {
    "ADMIN_PRINCIPAL": "Admin / Principal",
    "HOD": "Head of Department",
    "FACULTY": "Faculty",
    "STUDENT": "Student",
    "OFFICE_STAFF": "Office Staff",
    "LIBRARY_STAFF": "Library Staff",
}
PERMISSION_SEEDS = [
    ("MANAGE_USERS", "Manage users"),
    ("VIEW_COLLEGE_REPORTS", "View college-wide reports"),
    ("MANAGE_DEPARTMENTS", "Manage departments"),
    ("MANAGE_DEPARTMENT_FACULTY", "Manage department faculty"),
    ("VIEW_ASSIGNED_STUDENTS", "View assigned students"),
    ("MANAGE_ATTENDANCE", "Manage attendance"),
    ("MANAGE_MARKS", "Manage marks"),
    ("MANAGE_ADMISSIONS", "Manage admissions"),
    ("MANAGE_LIBRARY_BOOKS", "Manage library books"),
    ("MANAGE_LIBRARY_TRANSACTIONS", "Manage library transactions"),
]


def upgrade():
    op.add_column("roles", sa.Column("code", sa.String(length=50), nullable=True))
    op.add_column("users", sa.Column("email", sa.String(length=255), nullable=True))
    op.add_column("users", sa.Column("last_login_at", sa.DateTime(), nullable=True))
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_roles_code", "roles", ["code"], unique=True)
    conn = op.get_bind()
    conn.execute(sa.text("UPDATE roles SET code='ADMIN_PRINCIPAL' WHERE name='Admin/Principal' AND code IS NULL"))
    for code, name in ROLE_SEEDS.items():
        conn.execute(sa.text("INSERT INTO roles (code, name, created_at) SELECT :code, :name, CURRENT_TIMESTAMP WHERE NOT EXISTS (SELECT 1 FROM roles WHERE code=:code)"), {"code": code, "name": name})
    op.create_table("permissions", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("code", sa.String(100), nullable=False, unique=True), sa.Column("description", sa.String(255), nullable=False))
    op.create_table("role_permissions", sa.Column("role_id", sa.Integer(), sa.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True), sa.Column("permission_id", sa.Integer(), sa.ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True))
    op.create_table("audit_logs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("event_type", sa.String(80), nullable=False), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True), sa.Column("metadata_json", sa.JSON(), nullable=True), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_table("auth_tokens", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("jti_hash", sa.String(64), nullable=False, unique=True), sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("expires_at", sa.DateTime(), nullable=False), sa.Column("revoked_at", sa.DateTime(), nullable=True), sa.Column("created_at", sa.DateTime(), nullable=False))
    for code, description in PERMISSION_SEEDS:
        conn.execute(sa.text("INSERT INTO permissions (code, description) VALUES (:code, :description)"), {"code": code, "description": description})
    # Existing rows need a stable code; unknown legacy role names are preserved as generated codes.
    conn.execute(sa.text("UPDATE roles SET code=UPPER(REPLACE(REPLACE(name, '/', '_'), ' ', '_')) WHERE code IS NULL"))


def downgrade():
    op.drop_table("auth_tokens")
    op.drop_table("audit_logs")
    op.drop_table("role_permissions")
    op.drop_table("permissions")
    op.drop_index("ix_roles_code", table_name="roles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_column("users", "last_login_at")
    op.drop_column("users", "email")
    op.drop_column("roles", "code")
