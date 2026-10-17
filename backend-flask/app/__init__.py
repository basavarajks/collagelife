from app.admin.routes import admin_bp
from app.admin.scope_routes import admin_scope_bp
from app.api.routes import api_bp
from app.auth.routes import auth_bp
from app.hod.routes import hod_bp
from app.extensions import cors, db, migrate
