from app import create_app
from app.extensions import db
from app.models import Permission, Role, User

app = create_app()

ROLE_SEEDS = {
    "ADMIN_PRINCIPAL": "Admin / Principal",
    "HOD": "Head of Department",
    "FACULTY": "Faculty",
    "STUDENT": "Student",
    "OFFICE_STAFF": "Office Staff",
    "LIBRARY_STAFF": "Library Staff",
}

PERMISSION_SEEDS = {
    "MANAGE_USERS": "Manage users",
    "VIEW_COLLEGE_REPORTS": "View college-wide reports",
    "MANAGE_DEPARTMENTS": "Manage departments",
    "MANAGE_DEPARTMENT_FACULTY": "Manage department faculty",
    "VIEW_ASSIGNED_STUDENTS": "View assigned students",
    "MANAGE_ATTENDANCE": "Manage attendance",
    "MANAGE_MARKS": "Manage marks",
    "MANAGE_ADMISSIONS": "Manage admissions",
    "MANAGE_LIBRARY_BOOKS": "Manage library books",
    "MANAGE_LIBRARY_TRANSACTIONS": "Manage library transactions",
}


@app.cli.command("seed-admin")
def seed_admin():
    import click
    user_id = click.prompt("Admin user_id", type=str).strip()
    full_name = click.prompt("Admin full name", type=str).strip()
    password = click.prompt("Admin password", type=str, hide_input=True, confirmation_prompt=True)
    if User.query.filter_by(user_id=user_id).first():
        raise click.ClickException("User ID already exists.")
    role = Role.query.filter_by(code="ADMIN_PRINCIPAL").first()
    if not role:
        role = Role(code="ADMIN_PRINCIPAL", name=ROLE_SEEDS["ADMIN_PRINCIPAL"])
        db.session.add(role)
        db.session.flush()
    user = User(user_id=user_id, full_name=full_name, role=role, is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    click.echo("Administrator created successfully.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
