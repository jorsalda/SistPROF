import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from datetime import datetime
import logging

# Importar la función del worker
from app.services.notification_worker import process_pending_citaciones

# Variable GLOBAL para mantener el scheduler vivo
scheduler = None


def create_app():
    global scheduler  # Usar la variable global

    app = Flask(__name__)

    # ... tu configuración existente (config.from_object, etc.) ...

    # Configurar logging para ver debug del scheduler
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Crear scheduler solo si no existe
    if scheduler is None:
        scheduler = BackgroundScheduler(timezone='America/Bogota')

        # Agregar job con trigger explícito
        scheduler.add_job(
            func=process_pending_citaciones,
            trigger=IntervalTrigger(minutes=3),
            id='citacion_notifier',
            replace_existing=True,
            kwargs={'app': app},
            next_run_time=datetime.now()  # Ejecutar inmediatamente al iniciar
        )

        # Iniciar scheduler (FORZADO para pruebas)
        try:
            scheduler.start()
            logger.info("⏰ Scheduler de notificaciones INICIADO correctamente.")
            print("⏰ Scheduler de notificaciones INICIADO correctamente.")  # Doble garantía
        except Exception as e:
            logger.error(f"💥 Error al iniciar scheduler: {str(e)}")
            print(f"💥 Error al iniciar scheduler: {str(e)}")

    # ... resto de tu configuración (blueprints, etc.) ...

    return app