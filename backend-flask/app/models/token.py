from datetime import datetime, timezone

from app.extensions import db


class AuthToken(db.Model):
    __tablename__ = "auth_tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti_hash = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    expires_at = db.Column(db.DateTime, nullable=False, index=True)
    revoked_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    user = db.relationship("User", backref=db.backref("auth_tokens", lazy="dynamic"))

    @property
    def is_valid(self):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        expires = self.expires_at.replace(tzinfo=None) if self.expires_at.tzinfo else self.expires_at
        return self.revoked_at is None and expires > now
