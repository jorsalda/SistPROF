from flask import Flask, redirect, url_for
import os
from flask_login import current_user
from .extensions import db, login_manager
from flask_migrate import Migrate


migrate = Migrate()  # 👈 se declara una sola vez


def create_app():
    # Rutas absolutas
    base_dir = os.path.abspath(os.path.dirname(__file__))
    static_dir = os.path.join(base_dir, '..', 'static')

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder=static_dir,
        static_url_path='/static'
    )

    app.config.from_object('config.Config')

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)  # 👈 CORRECTO

    # 📌 IMPORTANTE: importar modelos (registro)
    from .models.usuario import Usuario
    from .models.colegio import Colegio
    from .models.docente import Docente
    from .models.permiso import Permiso

    # User loader
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(Usuario, int(user_id))

    # Blueprints
    from .routes.auth_routes import auth_bp
    from .routes.permiso_routes import permiso_bp
    from .routes.docente_routes import docente_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)

    # Ruta raíz
    @app.route("/")
    def index():
        return "SistPROF funcionando en Render 🚀"

    return app
