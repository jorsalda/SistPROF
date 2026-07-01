python3 -c "
from app import create_app
from app.extensions import db
from app.models.usuario import Usuario
from datetime import datetime, timedelta

app = create_app()
with app.app_context():
    usuarios = Usuario.query.all()
    for u in usuarios:
        u.is_approved = True
        u.failed_attempts = 0
        u.locked_until = None
        if not u.fecha_expiracion or u.fecha_expiracion < datetime.utcnow():
            u.fecha_expiracion = datetime.utcnow() + timedelta(days=30)
    db.session.commit()
    print(f'✅ {len(usuarios)} usuarios actualizados correctamente')
"