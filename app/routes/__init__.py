from flask import Flask, redirect, url_for
from flask_login import current_user
from config import Config

from app.extensions import db, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    login_manager.init_app(app)

    # --------- USER LOADER ---------
    from app.models.usuario import Usuario

    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id))

    # --------- REGISTRO DE BLUEPRINTS ---------
    from app.routes.auth_routes import bp as auth_bp
    from app.routes.permiso_routes import bp as permiso_bp
    from app.routes.docente_routes import bp as docente_bp  # ⭐⭐ Asegurar que está

    app.register_blueprint(auth_bp)
    app.register_blueprint(permiso_bp)
    app.register_blueprint(docente_bp)  # ⭐⭐ Asegurar que está

    # --------- RUTA RAÍZ CONDICIONAL ---------
    @app.route("/")
    def index():
        if current_user.is_authenticated:
            # ⭐⭐ REDIRIGIR SEGÚN ROL ⭐⭐
            if current_user.rol == 'admin':
                return redirect(url_for("docente.listar"))
            else:
                return redirect(url_for("permiso.listado"))
        return redirect(url_for("auth.login"))

    return app