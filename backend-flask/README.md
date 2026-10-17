# SDMS Phase 1 Flask Backend

This is a **separate Phase 1 backend foundation** added alongside the existing Django backend.

## Key endpoints

- `GET /api/v1/api/health`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/forgot-password` (returns not configured)
- `GET /api/v1/api/protected` (authorization header required)
- `GET /api/v1/api/principal-only` (Admin/Principal role required)

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
flask --app run.py db upgrade
flask --app run.py run
```

## Secure admin seed (local only)

```bash
flask --app run.py seed-admin
```

This command prompts for user ID, name, and password (no default credentials are created).
