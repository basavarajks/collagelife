import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret")
    TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")
    AUTH_TOKEN_COOKIE = os.getenv("AUTH_TOKEN_COOKIE", "sdms_auth")
    AUTH_COOKIE_SECURE = os.getenv("AUTH_COOKIE_SECURE", "false").lower() == "true"
    AUTH_COOKIE_SAMESITE = os.getenv("AUTH_COOKIE_SAMESITE", "Lax")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "sdms_db")

    _database_url = os.getenv("DATABASE_URL")
    if _database_url:
        SQLALCHEMY_DATABASE_URI = _database_url
        DATABASE_CONFIGURED = True
    elif DB_USER is not None and DB_PASSWORD is not None:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        DATABASE_CONFIGURED = True
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///sdms_phase2_dev.db"
        DATABASE_CONFIGURED = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DATABASE_CONFIGURED = True
    SECRET_KEY = "test-secret"
    AUTH_COOKIE_SECURE = False
