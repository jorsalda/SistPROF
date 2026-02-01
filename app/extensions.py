# app/extensions.py (MODIFÍCALO COMPLETO)
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

# ⭐ AÑADE el user_loader aquí mismo
@login_manager.user_loader
def load_user(user_id):
    # Import aquí para evitar circular
    from app.models.usuario import Usuario
    return db.session.get(Usuario, int(user_id))