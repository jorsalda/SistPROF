import os

from dotenv import load_dotenv

# Cargar variables de entorno desde .env (si existe)
load_dotenv()


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError(
            "La variable de entorno SECRET_KEY es obligatoria. "
            "Configúrala en tu archivo .env o con: fly secrets set SECRET_KEY=<tu_clave>"
        )

    # ✅ Clave de API para Google Gemini (IA)
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

    # Base de datos (local o producción)
    database_url = os.environ.get("SQLALCHEMY_DATABASE_URI")

    if not database_url:
        database_url = os.environ.get("DATABASE_URL")

    # Compatibilidad con Fly.io/Render/Heroku
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 300,
    }

    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
    MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", "false").lower() == "true"
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = FLASK_ENV == "development"

    SESSION_COOKIE_SECURE = FLASK_ENV == "production"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"