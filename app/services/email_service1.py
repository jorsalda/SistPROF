# app/services/email_service.py
from app.extensions import db
from app.services.notification_service import send_notification
from flask import url_for
import os


def send_reset_email(email, token):
    """
    Envía correo de restablecimiento usando el servicio centralizado.
    Mantiene compatibilidad total con las rutas actuales.
    """
    try:
        # Construir URL (ajusta el nombre del blueprint/ruta si tu estructura difiere)
        reset_url = url_for('auth.reset_password', token=token, _external=True)

        html_content = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: auto;">
            <h2 style="color: #2c3e50;">Restablecimiento de Contraseña</h2>
            <p>Hola,</p>
            <p>Has solicitado restablecer tu contraseña en <strong>SistPROF</strong>.</p>
            <p>Haz clic en el botón para continuar:</p>
            <a href="{reset_url}" 
               style="display:inline-block;padding:12px 24px;background:#0d6efd;color:#fff;text-decoration:none;border-radius:6px;font-weight:bold;">
               Restablecer Contraseña
            </a>
            <p style="margin-top: 20px; color: #6c757d; font-size: 0.9em;">
                Si no solicitaste este cambio, ignora este mensaje.<br>
                El enlace expira en 60 minutos.
            </p>
        </div>
        """

        # Delegar al nuevo servicio con auditoría
        resultado = send_notification(
            tipo='password_reset',
            destinatario=email,
            asunto='🔑 Restablecimiento de contraseña - SistPROF',
            html_content=html_content,
            token_id=None,  # Opcional: pasa el ID si lo consultas en BD
            payload_json={'accion': 'reset_password', 'origen': 'auth_flow'}
        )

        if resultado['success']:
            return True
        else:
            # Fallo manejado: no interrumpe la app, solo registra warning
            print(f"[AUTH WARNING] Email reset falló para {email}: {resultado.get('error')}")
            return False

    except Exception as e:
        # Safety net absoluto
        print(f"[AUTH CRITICAL] Error inesperado en send_reset_email: {str(e)}")
        return False