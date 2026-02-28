from flask import Flask
import os
from flask_login import current_user
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from werkzeug.middleware.proxy_fix import ProxyFix  # ✅ IMPORTANTE

from .extensions import db, login_manager, mail

migrate = Migrate()


def create_app():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder=static_dir,
        static_url_path='/static'
    )

    app.config.from_object('config.Config')

    # 🔥 FIX DEFINITIVO PARA RENDER (HTTPS + Proxy)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

    # 🔹 Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CSRFProtect(app)

    # 🔹 Rate limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"],
        storage_uri="memory://"
    )

    # 🔹 Importar modelos
    from .models.usuario import Usuario
    from .models.colegio import Colegio
    from .models.docente import Docente
    from .models.permiso import Permiso

    # 🔹 Crear tablas
    with app.app_context():
        db.create_all()

    # 🔹 User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # 🔹 Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.permiso_routes import permiso_bp
    from .routes.docente_routes import docente_bp
    from .routes.admin_routes import admin_bp
    from .routes.colegio_routes import colegio_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(colegio_bp)

    app.limiter = limiter

    return app