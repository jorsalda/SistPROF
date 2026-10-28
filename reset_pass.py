import sys
sys.path.insert(0, '.')

from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from werkzeug.security import generate_password_hash

app = create_app()

# --- CONFIGURACIÓN ---
NUEVO_EMAIL = 'jes-jr@jr.com'
NUEVA_PASSWORD = '123456'
# ---------------------

with app.app_context():
    usuario = Usuario.query.filter_by(email=NUEVO_EMAIL).first()
    
    if not usuario:
        print(f"❌ ERROR: No existe usuario con email {NUEVO_EMAIL}")
        sys.exit(1)

    # Actualizar contraseña
    usuario.password_hash = generate_password_hash(NUEVA_PASSWORD)
    
    # Desbloquear cuenta (por si acaso)
    if hasattr(usuario, 'failed_attempts'):
        usuario.failed_attempts = 0
    if hasattr(usuario, 'locked_until'):
        usuario.locked_until = None
    if hasattr(usuario, 'is_active'):
        usuario.is_active = True

    db.session.commit()
    print(f"✅ OK: Contraseña de {NUEVO_EMAIL} actualizada a: {NUEVA_PASSWORD}")
