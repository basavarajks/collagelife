from datetime import datetime, timezone

from app.extensions import db


class CollegeProfile(db.Model):
    __tablename__ = "college_profiles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    code = db.Column(db.String(50), nullable=True, unique=True)
    logo_path = db.Column(db.String(255), nullable=True)
    address = db.Column(db.Text, nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    contact_phone = db.Column(db.String(40), nullable=True)
    website = db.Column(db.String(255), nullable=True)
    description = db.Column(db.Text, nullable=True)
    established_year = db.Column(db.Integer, nullable=True)
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)
