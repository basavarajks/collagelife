from app.extensions import db


role_permissions = db.Table(
    "role_permissions",
    db.Column("role_id", db.Integer, db.ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    db.Column("permission_id", db.Integer, db.ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True),
)


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())

    users = db.relationship("User", back_populates="role", lazy="dynamic")
    permissions = db.relationship("Permission", secondary=role_permissions, back_populates="roles")

    def has_permission(self, code: str) -> bool:
        return any(permission.code == code for permission in self.permissions)
