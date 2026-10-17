import logging

from flask import Flask, jsonify

from app.api.routes import api_bp
from app.auth.routes import auth_bp
from app.extensions import cors, db, migrate


def create_app(config_object="app.config.Config"):
    app = Flask(__name__)
    app.config.from_object(config_object)

    _configure_logging(app)

    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": [app.config["FRONTEND_ORIGIN"]]}},
        supports_credentials=False,
    )

    app.register_blueprint(auth_bp)
    app.register_blueprint(api_bp)

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": {"message": "Not found"}}), 404

    @app.errorhandler(400)
    def bad_request(_error):
        return jsonify({"error": {"message": "Bad request"}}), 400

    @app.errorhandler(500)
    def internal(_error):
        app.logger.exception("Unhandled server error")
        return jsonify({"error": {"message": "Internal server error"}}), 500

    return app


def _configure_logging(app: Flask) -> None:
    if app.logger.handlers:
        return

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
