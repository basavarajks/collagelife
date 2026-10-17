from alembic import op
import sqlalchemy as sa

revision = "d4e5f6a7b8c9"
down_revision = "c3d4e5f6a7b8"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("hod_departments", sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False), sa.Column("department_id", sa.Integer(), sa.ForeignKey("departments.id", ondelete="CASCADE"), nullable=False), sa.PrimaryKeyConstraint("user_id", "department_id"))
    op.add_column("announcements", sa.Column("department_id", sa.Integer(), nullable=True))
    op.create_foreign_key("fk_announcements_department_id", "announcements", "departments", ["department_id"], ["id"], ondelete="CASCADE")
    op.create_index("ix_announcements_department_id", "announcements", ["department_id"])


def downgrade():
    op.drop_index("ix_announcements_department_id", table_name="announcements")
    op.drop_constraint("fk_announcements_department_id", "announcements", type_="foreignkey")
    op.drop_column("announcements", "department_id")
    op.drop_table("hod_departments")
