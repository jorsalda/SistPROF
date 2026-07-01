import os
from pathlib import Path

# Cargar .env en desarrollo
if os.environ.get("FLASK_ENV") != "production":
    from dotenv import load_dotenv

    BASE_DIR = Path(__file__).resolve().parent
    load_dotenv(BASE_DIR / ".env")


class Config:
    # Seguridad
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "clave_super_segura"
    )

    # Base de datos
    database_url = os.environ.get(
        "SQLALCHEMY_DATABASE_URI"
    )

    if not database_url:
        database_url = os.environ.get(
            "DATABASE_URL"
        )

    # Compatibilidad con Render/Heroku
    if (
        database_url
        and database_url.startswith("postgres://")
    ):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    # Debug temporal (después lo quitamos)
    print("DATABASE CARGADA:", database_url)

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    # Correo
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(
        os.environ.get("MAIL_PORT", 587)
    )
    MAIL_USE_TLS = (
        os.environ.get(
            "MAIL_USE_TLS",
            "true"
        ).lower() == "true"
    )
    MAIL_USE_SSL = (
        os.environ.get(
            "MAIL_USE_SSL",
            "false"
        ).lower() == "true"
    )

    MAIL_USERNAME = os.environ.get(
        "MAIL_USERNAME"
    )
    MAIL_PASSWORD = os.environ.get(
        "MAIL_PASSWORD"
    )

    MAIL_DEFAULT_SENDER = os.environ.get(
        "MAIL_DEFAULT_SENDER",
        MAIL_USERNAME
    )

    # Entorno
    FLASK_ENV = os.environ.get(
        "FLASK_ENV",
        "development"
    )

    DEBUG = FLASK_ENV == "development"

    # Sesiones
    SESSION_COOKIE_SECURE = (
        FLASK_ENV == "production"
    )
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"