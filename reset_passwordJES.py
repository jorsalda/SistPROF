from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    usuario = Usuario.query.get(50)

    if usuario:
        nueva_password = "Jes8026##"  # O la que quieras
        usuario.password_hash = generate_password_hash(nueva_password)
        db.session.commit()

        print(f"✅ Contraseña de {usuario.email} actualizada a: {nueva_password}")
    else:
        print("❌ Usuario no encontrado")