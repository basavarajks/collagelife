import pytest

from app import create_app
from app.extensions import db
from app.models import Role, User


@pytest.fixture()
def app():
    app = create_app("app.config.TestingConfig")

    with app.app_context():
        db.create_all()

        role = Role(name="Student")
        db.session.add(role)
        db.session.flush()

        user = User(user_id="student1", full_name="Student Demo", role_id=role.id, is_active=True)
        user.set_password("pass1234")
        db.session.add(user)
        db.session.commit()

        yield app

        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
