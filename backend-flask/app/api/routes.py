from flask import Blueprint, jsonify, g

from app.auth.utils import auth_required


api_bp = Blueprint("api", __name__, url_prefix="/api/v1/api")


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok", "service": "sdms-phase1-auth"})


@api_bp.get("/protected")
@auth_required()
def protected():
    return jsonify(
        {
            "data": {
                "message": "Protected access granted",
                "user_id": g.current_user.user_id,
                "role": g.current_user.role.name,
            }
        }
    )


@api_bp.get("/principal-only")
@auth_required(roles=["Admin/Principal"])
def principal_only():
    return jsonify({"data": {"message": "Principal/Admin authorized endpoint"}})
