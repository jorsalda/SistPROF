from flask import Flask
import os
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix
from .extensions import db, login_manager, mail
from app.routes.examen_routes import examen_bp

# Blueprints
from app.routes.estudiantes_routes import estudiante_bp
from app.routes.coordinador_routes import coordinador_bp


from .models.pregunta import Pregunta
# Modelos
from .models import *

migrate = Migrate()


def create_app():

    base_dir = os.path.abspath(os.path.dirname(__file__))

    static_dir = os.path.join(
        base_dir,
        "..",
        "static"
    )

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder=static_dir,
        static_url_path="/static"
    )

    app.config.from_object("config.Config")

    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_proto=1,
        x_host=1
    )

    # -----------------------------------------
    # Inicializar extensiones
    # -----------------------------------------

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    CSRFProtect(app)

    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=[
            "200 per day",
            "50 per hour"
        ],
        storage_uri="memory://"
    )

    # -----------------------------------------
    # Login manager
    # -----------------------------------------

    @login_manager.user_loader
    def load_user(user_id):

        return db.session.get(
            Usuario,
            int(user_id)
        )

    # -----------------------------------------
    # Blueprints
    # -----------------------------------------

    from .routes.auth_routes import auth_bp
    from .routes.permiso_routes import permiso_bp
    from .routes.docente_routes import docente_bp
    from .routes.admin_routes import admin_bp
    from .routes.colegio_routes import colegio_bp
    from app.routes.api_examen_bp import api_examen_bp

    from .routes.acudiente import acudiente_bp
    from .routes.api_acudiente import api_acudiente_bp

    # ... dentro de create_app(), donde están los otros registros:


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
    app.limiter = limiter

    # ==========================================
    # Scheduler de notificaciones
    # ==========================================

    from apscheduler.schedulers.background import (
        BackgroundScheduler
    )

    from datetime import datetime

    import logging

    logger = logging.getLogger(__name__)

    scheduler = BackgroundScheduler(
        timezone='America/Bogota'
    )

    try:

        from app.services.notification_worker import (
            process_pending_citaciones
        )

        scheduler.add_job(
            func=process_pending_citaciones,
            trigger='interval',
            minutes=3,
            id='citacion_notifier',
            replace_existing=True,
            kwargs={'app': app},
            next_run_time=datetime.now()
        )

        scheduler.start()

        print(
            "⏰ Scheduler de notificaciones INICIADO."
        )

    except Exception as e:

        print(
            f"⚠️ Scheduler no iniciado: {str(e)}"
        )

    # ==========================================

    return app