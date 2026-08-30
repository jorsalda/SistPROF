# app/__init__.py
# =============================================================================
# Aplicación Principal SistPROF
# =============================================================================

import os
import logging
import atexit
from datetime import datetime

from flask import Flask, render_template
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from apscheduler.schedulers.background import BackgroundScheduler

# Extensiones centrales
from .extensions import db, login_manager, mail

logger = logging.getLogger(__name__)
migrate = Migrate()


def create_app():
    """Factory principal de la aplicación Flask."""

    # -------------------------------------------------------------------------
    # 1. CONFIGURACIÓN DE FLASK
    # -------------------------------------------------------------------------
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, "..", "static")

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder=static_dir,
        static_url_path="/static"
    )
    app.config.from_object("config.Config")
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # -------------------------------------------------------------------------
    # 2. EXTENSIONES
    # -------------------------------------------------------------------------
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Rate limiting
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri=os.environ.get("REDIS_URL", "memory://")
    )
    app.limiter = limiter

    # -------------------------------------------------------------------------
    # 3. LOGIN MANAGER
    # -------------------------------------------------------------------------
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.usuario import Usuario
        return db.session.get(Usuario, int(user_id))

    # -------------------------------------------------------------------------
    # 4. BLUEPRINTS (Importaciones locales para evitar conflictos)
    # -------------------------------------------------------------------------
    try:
        from .routes.acudiente import acudiente_bp
        from .routes.admin_routes import admin_bp
        from .routes.api_acudiente import api_acudiente_bp
        from .routes.api_examen_bp import api_examen_bp
        from .routes.auth_routes import auth_bp
        from .routes.colegio_routes import colegio_bp
        from .routes.coordinador_routes import coordinador_bp
        from .routes.docente_routes import docente_bp

        # ✅ IMPORTACIÓN CRÍTICA: Debe coincidir con estudiantes_routes.py
        from .routes.estudiantes_routes import estudiante_bp

        from .routes.examen_routes import examen_bp
        from .routes.membresia_routes import membresia_bp
        from .routes.permiso_routes import permiso_bp
    except ImportError as e:
        logger.error(f"❌ ERROR CRÍTICO AL IMPORTAR BLUEPRINTS: {e}")
        raise

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(colegio_bp)
    app.register_blueprint(estudiante_bp)
    app.register_blueprint(coordinador_bp)
    app.register_blueprint(examen_bp)
    app.register_blueprint(api_examen_bp)
    app.register_blueprint(acudiente_bp)
    app.register_blueprint(api_acudiente_bp)
    app.register_blueprint(membresia_bp)

    # -------------------------------------------------------------------------
    # 5. CSRF
    # -------------------------------------------------------------------------
    csrf = CSRFProtect(app)
    csrf.exempt(api_examen_bp)
    csrf.exempt(api_acudiente_bp)

    # -------------------------------------------------------------------------
    # 6. MANEJADORES DE ERROR
    # -------------------------------------------------------------------------
    @app.errorhandler(404)
    def pagina_no_encontrada(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def error_interno(error):
        return render_template("errors/500.html"), 500

    # -------------------------------------------------------------------------
    # 7. SCHEDULER DE NOTIFICACIONES
    # -------------------------------------------------------------------------
    scheduler = BackgroundScheduler(timezone='America/Bogota')

    try:
        from app.services.notification_worker import process_pending_citations
        scheduler.add_job(
            func=process_pending_citations,
            trigger='interval',
            minutes=3,
            id='citacion_notifier',
            replace_existing=True,
            kwargs={'app': app},
            next_run_time=datetime.now()
        )
        scheduler.start()
        logger.info("✅ Scheduler de notificaciones INICIADO.")
        atexit.register(lambda: scheduler.shutdown())
    except Exception as e:
        logger.error(f"⚠️ Scheduler no iniciado: {str(e)}")

    return app