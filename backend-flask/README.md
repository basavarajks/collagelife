# Phase 2 authentication and RBAC

Phase 2 extends the Phase 1 React/Flask foundation without replacing the existing Flutter or Django applications.

## Backend setup on Windows PowerShell

```powershell
cd .\backend-flask
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
# Edit .env: set SECRET_KEY and DATABASE_URL (or DB_* values)
flask --app run.py db upgrade
flask --app run.py seed-admin
flask --app run.py run
```

Start MySQL in XAMPP first and create/select `sdms_db` in phpMyAdmin. Verify the actual MySQL port, username, and password rather than assuming XAMPP defaults. Never edit the XAMPP data directory.

## Frontend setup

In another PowerShell window:

```powershell
cd .\frontend-react
npm install
copy .env.example .env
npm run dev
```

Phase 2 uses signed bearer tokens with a server-side token registry so logout revokes the token. The React app keeps the short-lived token in session storage only and reloads the user through `/api/v1/auth/me`; it does not trust a stored role. For production, prefer HTTPS, a secure HttpOnly cookie deployment, and an appropriate CSRF strategy. `AUTH_USE_COOKIE=false` is intended for local development.

Endpoints include `/api/v1/auth/login`, `/logout`, `/me`, `/change-password`, `/api/v1/api/health`, protected examples, and permission/role examples. Password reset remains intentionally unconfigured. `seed-admin` is a local CLI command and never runs automatically.

The migration adds normalized role codes, six role records, permissions, role-permission relationships, audit logs, token revocation records, email, and last-login tracking. No dashboards or SDMS business modules are included in Phase 2.
