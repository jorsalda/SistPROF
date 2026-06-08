    SistPROF/
    │
    ├── 📁 middleware/
    │   ├── __init__.py
    │   ├── auth_middleware.py
    │   └── superuser_middleware.py
    │
    ├──  models/
    │   ├── __init__.py
    │   ├── acudiente.py
    │   ├── acuerdo_correctivo.py
    │   ├── acuerdo_evaluacion.py
    │   ├── ajuste_razonable.py
    │   ├── alerta.py
    │   ├── areas_gestion.py
    │   ├── asistencias.py
    │   ├── citacion_acudiente.py
    │   ├── clase.py
    │   ├── clase_estudiante.py
    │   ├── colegio.py
    │   ├── competencia_materia.py
    │   ├── competencias.py
    │   ├── configuracion_disciplinaria.py
    │   ├── configuracion_escalamiento.py
    │   ├── contribucion.py
    │   ├── coordinador.py
    │   ├── criterio_evaluacion.py
    │   ├── descargo_estudiante.py
    │   ├── docente.py
    │   ├── escala_evaluacion.py
    │   ├── estudiante.py
    │   ├── estudiante_acudiente.py
    │   ├── evaluacion_criterio.py
    │   ├── evaluacion_estudiante.py
    │   ├── evaluacion_final.py
    │   ├── evidencia.py
    │   ├── examen.py
    │   ├── indicador_logro.py
    │   ├── ingreso_colegio.py
    │   ├── jornada.py
    │   ├── justificacion_acudiente.py
    │   ├── materia.py
    │   ├── notification_log.py
    │   ├── novedad.py
    │   ├── periodo.py
    │   ├── periodo_academico.py
    │   ├── permiso.py
    │   ├── piar.py
    │   ├── respuesta_novedad.py
    │   ├── resultado_examen.py
    │   ├── sede.py
    │   ├── seguimiento.py
    │   ├── suscripcion.py
    │   ├── token_activacion.py
    │   └── usuario.py
    │
    ├──  routes/
    │   ├── __init__.py
    │   ├── admin_routes.py
    │   ├── auth_routes.py
    │   ├── auth_service.py
    │   ├── colegio_routes.py
    │   ├── colegio_routes1.py
    │   ├── coordinador_routes.py
    │   ├── docente_routes.py
    │   ├── docs_routes.py
    │   ├── estudiantes_routes.py
    │   └── permiso_routes.py
    │
    ├──  services/
    │   ├── __init__.py
    │   ├── auth_service.py
    │   ├── email_service.py
    │   ├── email_service1.py
    │   ├── notification_service.py
    │   ├── notification_worker.py
    │   └── notification_worker1.py
    │
    ├──  templates/
    │   └── (archivos HTML de plantillas)
    │
    ├──  utils/
    │   └── __init__.py
    │
    ├── 📁 docs/
    │
    ├──  migrations/
    │
    ── 📁 static/
    │   ├── css/
    │   ├── js/
    │   └── (archivos estáticos)
    │
    ├──  ARCHIVOS DE CONFIGURACIÓN Y RAÍZ:
    ├── __init__.py
    ├── extensions.py
    ├── run.py                    # Punto de entrada principal
    ├── wsgi.py                   # WSGI para producción
    ├── config.py                 # Configuración principal
    ├── config1.py                # Configuración alternativa
    ├── connexion.py              # Conexión a BD
    ├── ejecutar.py               # Script de ejecución
    ├── reset_password.py         # Reset de contraseña
    ├── reset_passwordL.py        # Otra versión de reset
    │
    ├──  ARCHIVOS DE ENTORNO:
    ├── .env                      # Variables de entorno
    ├── .env1                     # Variables alternativas
    ├── .gitignore                # Git ignore
    │
    ├── 📄 ARCHIVOS DE DESPLIEGUE:
    ├── Procfile                  # Para Heroku/Render
    ├── fly.toml                  # Para Fly.io
    ├── requirements.txt          # Dependencias Python
    ├── runtime.txt               # Versión de Python
    │
    └── 📄 OTROS:
        ├── presentacion.html     # Presentación
        └── Procfila              # (posible duplicado)