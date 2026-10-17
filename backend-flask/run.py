from app import create_app
from app.extensions import db
from app.models import Role, User

app = create_app()


@app.cli.command("seed-admin")
def seed_admin():
    import click

    user_id = click.prompt("Admin user_id", type=str).strip()
    full_name = click.prompt("Admin full name", type=str).strip()
    password = click.prompt("Admin password", type=str, hide_input=True, confirmation_prompt=True)

    role = Role.query.filter_by(name="Admin/Principal").first()
    if role is None:
        role = Role(name="Admin/Principal")
        db.session.add(role)
        db.session.flush()

    existing = User.query.filter_by(user_id=user_id).first()
    if existing:
        raise click.ClickException("User ID already exists. Use a different user_id.")

    user = User(user_id=user_id, full_name=full_name, role_id=role.id, is_active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    click.echo("Admin user created successfully.")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
