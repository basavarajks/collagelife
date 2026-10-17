from flask import Flask, jsonify
from flask_cors import CORS
import logging

from app.api.routes import api_bp
from app.auth.routes import auth_bp
from app.extensions import cors, db, migrate


def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app, resources={r"/api/*": {"origins": [app.config["FRONTEND_ORIGIN"]]}}, supports_credentials=app.config.get("AUTH_USE_COOKIE", False))
    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": {"message": "Not found"}}), 404

    @app.errorhandler(500)
    def internal(_error):
        app.logger.exception("Unhandled server error")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    return app
