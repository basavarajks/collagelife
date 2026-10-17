from alembic import op
import sqlalchemy as sa

revision = "c3d4e5f6a7b8"
down_revision = "a1b2c3d4e5f6"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("college_profiles", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(200), nullable=False), sa.Column("code", sa.String(50), nullable=True, unique=True), sa.Column("logo_path", sa.String(255), nullable=True), sa.Column("address", sa.Text(), nullable=True), sa.Column("contact_email", sa.String(255), nullable=True), sa.Column("contact_phone", sa.String(40), nullable=True), sa.Column("website", sa.String(255), nullable=True), sa.Column("description", sa.Text(), nullable=True), sa.Column("established_year", sa.Integer(), nullable=True), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_table("departments", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("code", sa.String(30), nullable=False), sa.Column("name", sa.String(160), nullable=False), sa.Column("description", sa.Text(), nullable=True), sa.Column("head_user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True), sa.Column("is_active", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False), sa.UniqueConstraint("code"))
    op.create_index("ix_departments_code", "departments", ["code"], unique=True)
    op.create_index("ix_departments_is_active", "departments", ["is_active"])
    op.create_table("academic_years", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("name", sa.String(40), nullable=False, unique=True), sa.Column("start_date", sa.Date(), nullable=False), sa.Column("end_date", sa.Date(), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("is_current", sa.Boolean(), nullable=False), sa.Column("created_at", sa.DateTime(), nullable=False))
    op.create_index("ix_academic_years_is_current", "academic_years", ["is_current"])
    op.create_table("semesters", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("academic_year_id", sa.Integer(), sa.ForeignKey("academic_years.id", ondelete="CASCADE"), nullable=False), sa.Column("number", sa.Integer(), nullable=False), sa.Column("name", sa.String(80), nullable=False), sa.Column("start_date", sa.Date(), nullable=False), sa.Column("end_date", sa.Date(), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.UniqueConstraint("academic_year_id", "number", name="uq_semester_year_number"))
    op.create_table("announcements", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("title", sa.String(200), nullable=False), sa.Column("message", sa.Text(), nullable=False), sa.Column("publish_at", sa.DateTime(), nullable=True), sa.Column("expires_at", sa.DateTime(), nullable=True), sa.Column("audience", sa.String(100), nullable=False), sa.Column("status", sa.String(20), nullable=False), sa.Column("created_by", sa.Integer(), sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True), sa.Column("created_at", sa.DateTime(), nullable=False), sa.Column("updated_at", sa.DateTime(), nullable=False))
    op.create_index("ix_announcements_status", "announcements", ["status"])


def downgrade():
    op.drop_index("ix_announcements_status", table_name="announcements")
    op.drop_table("announcements")
    op.drop_table("semesters")
    op.drop_index("ix_academic_years_is_current", table_name="academic_years")
    op.drop_table("academic_years")
    op.drop_index("ix_departments_is_active", table_name="departments")
    op.drop_index("ix_departments_code", table_name="departments")
    op.drop_table("departments")
    op.drop_table("college_profiles")
