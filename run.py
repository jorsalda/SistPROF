# run.py - VERSIÓN MEJORADA
import os
import sys
import traceback
from flask import Flask
from app.extensions import db, login_manager
from app.routes.auth_routes import auth_bp
from app.routes.permiso_routes import permiso_bp
from config import Config
from app.models.usuario import Usuario
from app.routes.docente_routes import docente_bp



def create_app():
    # Especificar ruta de templates
    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, 'app', 'templates')

    app = Flask(__name__, template_folder=template_path)

    try:
        app.config.from_object(Config)

        db.init_app(app)
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(user_id):
            return Usuario.query.get(int(user_id))

        app.register_blueprint(auth_bp)
        app.register_blueprint(permiso_bp)
        app.register_blueprint(docente_bp)
        # Crear tablas - solo mensaje si es primera ejecución
        with app.app_context():
            db.create_all()
            if not os.environ.get('WERKZEUG_RUN_MAIN'):
                print("✅ Tablas creadas/verificadas")

        return app

    except Exception as e:
        print(f"❌ ERROR: {e}")
        traceback.print_exc()
        sys.exit(1)


app = create_app()

if __name__ == '__main__':
    # Esta condición evita que se imprima dos veces


    app.run(debug=True)