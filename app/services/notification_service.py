from app.extensions import db
from app.models.notification_log import NotificationLog
from datetime import datetime
import os

# Importar Resend (ya lo tienes configurado)
try:
    import resend

    resend.api_key = os.getenv('RESEND_API_KEY')
    RESEND_ENABLED = True
except ImportError:
    RESEND_ENABLED = False


def send_notification(tipo, destinatario, asunto, html_content,
                      citacion_id=None, token_id=None, payload_json=None):
    """
    Envía una notificación por email y registra el log en la BD.

    Args:
        tipo: 'password_reset', 'citacion_acudiente', 'ingreso_qr', etc.
        destinatario: Email del destinatario
        asunto: Asunto del correo
        html_content: Contenido HTML del email
        citacion_id: ID de citación (si aplica)
        token_id: ID de token (si aplica)
        payload_json: Datos adicionales en formato dict

    Returns:
        dict: {'success': bool, 'log_id': int, 'error': str|None}
    """

    log_entry = None
    from_email = os.getenv('RESEND_FROM_EMAIL', 'noreply@tuapp.com')

    try:
        # 1. Crear registro en notification_logs (estado='pendiente')
        log_entry = NotificationLog(
            tipo=tipo,
            destinatario=destinatario,
            asunto=asunto,
            estado='pendiente',
            citacion_id=citacion_id,
            token_id=token_id,
            payload_json=payload_json,
            proveedor='resend',
            fecha_creacion=datetime.utcnow()
        )
        db.session.add(log_entry)
        db.session.flush()  # Obtiene el ID sin hacer commit aún

        # 2. Enviar email vía Resend
        if RESEND_ENABLED:
            email_response = resend.Emails.send({
                "from": from_email,
                "to": destinatario,
                "subject": asunto,
                "html": html_content
            })

            # 3. Actualizar log con éxito
            log_entry.estado = 'enviado'
            log_entry.id_proveedor = email_response.get('id')
            log_entry.fecha_actualizacion = datetime.utcnow()

            db.session.commit()

            return {
                'success': True,
                'log_id': log_entry.id,
                'provider_id': email_response.get('id'),
                'error': None
            }
        else:
            # Modo sin Resend (desarrollo/testing)
            log_entry.estado = 'pendiente'
            log_entry.error_msg = 'Resend no configurado - modo desarrollo'
            db.session.commit()

            return {
                'success': False,
                'log_id': log_entry.id,
                'error': 'Resend API no disponible',
                'dev_mode': True
            }

    except Exception as e:
        # 4. Si algo falla, registrar error y hacer rollback
        db.session.rollback()

        error_message = str(e)

        # Intentar guardar el error en el log (si log_entry existe)
        if log_entry and log_entry.id:
            try:
                log_entry.estado = 'fallido'
                log_entry.error_msg = error_message[:500]  # Máximo 500 chars
                log_entry.fecha_actualizacion = datetime.utcnow()
                db.session.commit()
            except:
                db.session.rollback()

        return {
            'success': False,
            'log_id': log_entry.id if log_entry else None,
            'error': error_message
        }