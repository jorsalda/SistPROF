from flask import Flask
import os
from app.extensions import db, login_manager


def create_app():
    # ✅ Configurar rutas absolutas para static_folder
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(__name__,
                template_folder="templates",
                static_folder=static_dir,
                static_url_path='/static')

    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # ⭐⭐ IMPORTANTE: Importar modelos AQUÍ para registrarlos una sola vez
    from app.models.usuario import Usuario
    from app.models.colegio import Colegio
    from app.models.docente import Docente
    from app.models.permiso import Permiso

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.permiso_routes import permiso_bp
    from app.routes.docente_routes import docente_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)

    # Ruta raíz
    from flask import redirect, url_for
    from flask_login import current_user

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            return redirect(url_for("permiso.listado"))  # ← AQUÍ
        return redirect(url_for("auth.login"))

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app