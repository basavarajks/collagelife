import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-change-this-secret")
    TOKEN_TTL_SECONDS = int(os.getenv("TOKEN_TTL_SECONDS", "3600"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5173")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "sdms_db")

    _database_url = os.getenv("DATABASE_URL")
    if _database_url:
        SQLALCHEMY_DATABASE_URI = _database_url
        DATABASE_CONFIGURED = True
    elif DB_USER and DB_PASSWORD:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        DATABASE_CONFIGURED = True
    else:
        SQLALCHEMY_DATABASE_URI = "sqlite:///sdms_phase1_dev.db"
        DATABASE_CONFIGURED = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    DATABASE_CONFIGURED = True
    SECRET_KEY = "test-secret"
