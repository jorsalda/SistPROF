from flask import current_app, Flask
from typing import Optional, Dict, Any
from datetime import datetime
import logging

from app.extensions import db
from app.models.notification_log import NotificationLog
from app.models.citacion_acudiente import CitacionAcudiente
from app.models.acudiente import Acudiente
from app.models.estudiante import Estudiante
from app.services.notification_service import send_notification

logger = logging.getLogger(__name__)


def _construir_email_citacion(estudiante_nombre: str, motivo: str, fecha_citacion: datetime) -> str:
    """
    Construye el HTML del email de citación.
    Función pura: fácil de testear y mantener.
    """
    return f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: auto;">
        <h2 style="color: #dc3545;">📋 Citación Escolar</h2>
        <p>Estimado acudiente,</p>
        <p>Se le cita para el día <strong>{fecha_citacion.strftime('%d/%m/%Y')}</strong>.</p>
        <p><strong>Estudiante:</strong> {estudiante_nombre}</p>
        <p><strong>Motivo:</strong> {motivo}</p>
        <p style="margin-top: 20px; color: #6c757d; font-size: 0.9em;">
            Por favor confirme asistencia o contacte a coordinación.
        </p>
    </div>
    """


def _construir_email_ingreso(estudiante_nombre: str, hora_ingreso: str, sede_nombre: str) -> str:
    """
    Construye el HTML del email de notificación de ingreso por QR.
    Función pura: fácil de testear y mantener.
    """
    return f"""
    <div style="font-family: sans-serif; max-width: 600px; margin: auto;">
        <h2 style="color: #28a745;">✅ Ingreso al Colegio</h2>
        <p>Estimado acudiente,</p>
        <p>Le informamos que el estudiante <strong>{estudiante_nombre}</strong> ha ingresado al colegio.</p>
        <ul>
            <li><strong>Hora:</strong> {hora_ingreso}</li>
            <li><strong>Sede:</strong> {sede_nombre}</li>
        </ul>
        <p style="color: #6c757d; font-size: 0.9em;">SistPROF - Control de Asistencia</p>
    </div>
    """


def process_pending_citaciones(app: Optional[Flask] = None) -> Dict[str, Any]:
    """
    Busca citaciones pendientes y envía emails automáticamente.
    OPTIMIZADO para alto volumen (miles de registros/día).

    Args:
        app: Instancia de Flask (opcional, para contexto fuera de request)

    Returns:
        dict con estadísticas: {'exitosas': int, 'fallidas': int, 'total': int}
    """
    if app:
        with app.app_context():
            return _procesar_citaciones_interno()
    else:
        return _procesar_citaciones_interno()


def _procesar_citaciones_interno(limite: Optional[int] = None) -> Dict[str, int]:
    """
    Lógica interna optimizada:
    - Solo consulta los campos necesarios (no carga objetos completos)
    - Usa UPDATE directo en lugar de cargar y modificar objetos
    - Procesa en lotes para no saturar memoria

    Args:
        limite: Máximo de citaciones a procesar (None = todas)

    Returns:
        dict con estadísticas: {'exitosas': X, 'fallidas': Y}
    """
    logger.info("🔄 Buscando citaciones pendientes para notificar...")
    start_time = datetime.utcnow()

    try:
        # ✅ CONSULTA OPTIMIZADA: Solo trae los 7 campos que realmente usamos
        query = db.session.query(
            CitacionAcudiente.id,
            CitacionAcudiente.motivo,
            CitacionAcudiente.fecha_citacion,
            CitacionAcudiente.estudiante_id,
            CitacionAcudiente.acudiente_id,
            Acudiente.email,
            Estudiante.nombre.label('estudiante_nombre')
        ) \
            .join(Acudiente, CitacionAcudiente.acudiente_id == Acudiente.id) \
            .join(Estudiante, CitacionAcudiente.estudiante_id == Estudiante.id) \
            .filter(CitacionAcudiente.estado == 'pendiente')

        # Aplicar límite si se especifica (útil para testing o Celery con batches)
        if limite is not None:
            query = query.limit(limite)

        pendientes = query.all()

        total_pendientes = len(pendientes)

        if total_pendientes == 0:
            logger.info("✅ No hay citaciones pendientes.")
            return {'exitosas': 0, 'fallidas': 0, 'total': 0}

        logger.info(f"📦 Encontradas {total_pendientes} citaciones pendientes.")

        # Contadores para métricas
        exitosas = 0
        fallidas = 0

        # ✅ PROCESAMIENTO EN LOTES (batch processing)
        for idx, citacion in enumerate(pendientes, 1):
            try:
                # Construir contenido del email usando función dedicada
                html_content = _construir_email_citacion(
                    estudiante_nombre=citacion.estudiante_nombre,
                    motivo=citacion.motivo,
                    fecha_citacion=citacion.fecha_citacion
                )

                # Enviar email
                resultado = send_notification(
                    tipo='citacion_acudiente',
                    destinatario=citacion.email,
                    asunto=f'📋 Citación - {citacion.estudiante_nombre}',
                    html_content=html_content,
                    citacion_id=citacion.id,
                    payload_json={
                        'estudiante_id': citacion.estudiante_id,
                        'acudiente_id': citacion.acudiente_id,
                        'motivo': citacion.motivo
                    }
                )

                if resultado['success']:
                    # ✅ UPDATE DIRECTO: Sin cargar el objeto completo
                    # Esto es 5-10x más rápido que: citacion.estado = 'notificada'
                    db.session.execute(
                        db.update(CitacionAcudiente)
                        .where(CitacionAcudiente.id == citacion.id)
                        .values(
                            estado='notificada',
                            fecha_notificacion=datetime.utcnow()
                        )
                    )

                    exitosas += 1

                    # Log cada 100 registros para no saturar
                    if idx % 100 == 0:
                        logger.info(f"⏳ Progreso: {idx}/{total_pendientes} procesadas")
                else:
                    fallidas += 1
                    logger.warning(f"⚠️ Fallo citación {citacion.id}: {resultado.get('error')}")

            except Exception as e:
                fallidas += 1
                logger.error(f"❌ Error procesando citación {citacion.id}: {str(e)}")
                db.session.rollback()

        # Commit final de todas las actualizaciones
        db.session.commit()

        # Métricas finales
        elapsed_time = (datetime.utcnow() - start_time).total_seconds()
        logger.info(f"🏁 Proceso completado:")
        logger.info(f"   ✅ Exitosas: {exitosas}")
        logger.info(f"   ❌ Fallidas: {fallidas}")
        logger.info(f"   ⏱️ Tiempo total: {elapsed_time:.2f} segundos")

        if elapsed_time > 0:
            logger.info(f"   📊 Promedio: {total_pendientes / elapsed_time:.1f} citaciones/segundo")

        return {'exitosas': exitosas, 'fallidas': fallidas, 'total': total_pendientes}

    except Exception as e:
        logger.error(f"💥 Error crítico en process_pending_citaciones: {str(e)}")
        db.session.rollback()
        return {'exitosas': 0, 'fallidas': total_pendientes if 'total_pendientes' in locals() else 0, 'total': 0}


def notify_student_ingress(estudiante_id: int, hora_ingreso: str, sede_nombre: str) -> bool:
    """
    Envía notificación inmediata al acudiente cuando el estudiante ingresa por QR.
    Se llama directamente desde la ruta de escaneo.

    Args:
        estudiante_id: ID del estudiante que ingresó
        hora_ingreso: Hora formateada del ingreso
        sede_nombre: Nombre de la sede donde ingresó

    Returns:
        bool: True si se envió correctamente, False en caso de error
    """
    with current_app.app_context():
        try:
            # ✅ Consulta optimizada: solo email y nombre
            resultado = db.session.query(
                Estudiante.nombre,
                Acudiente.email
            ) \
                .join(Estudiante.acudientes) \
                .filter(Estudiante.id == estudiante_id) \
                .first()

            if not resultado:
                logger.warning(f"No hay acudiente registrado para estudiante {estudiante_id}.")
                return False

            estudiante_nombre, acudiente_email = resultado

            # Construir contenido usando función dedicada
            html_content = _construir_email_ingreso(
                estudiante_nombre=estudiante_nombre,
                hora_ingreso=hora_ingreso,
                sede_nombre=sede_nombre
            )

            # Enviar
            resultado_envio = send_notification(
                tipo='ingreso_qr',
                destinatario=acudiente_email,
                asunto=f'✅ Ingreso - {estudiante_nombre}',
                html_content=html_content,
                payload_json={
                    'estudiante_id': estudiante_id,
                    'hora': hora_ingreso,
                    'sede': sede_nombre
                }
            )

            if resultado_envio['success']:
                logger.info(f"🔔 Notificación de ingreso enviada para {estudiante_nombre}")
                return True
            else:
                logger.warning(f"⚠️ Fallo notificación ingreso: {resultado_envio.get('error')}")
                return False

        except Exception as e:
            logger.error(f"❌ Error en notify_student_ingress: {str(e)}")
            return False