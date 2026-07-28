(.venv) jorge@jorge-Latitude-7430:~/PycharmProjects/SistPROF$ tree -L 2 -I '__pycache__|*.pyc|venv|.venv|migrations|node_modules' app/
app/
├── extensions.py
├── __init__.py
├── middleware
│   ├── auth_middleware.py
│   ├── __init__.py
│   └── superuser_middleware.py
├── models
│   ├── acudiente.py
│   ├── acuerdo_correctivo.py
│   ├── acuerdo_evaluacion.py
│   ├── ajuste_razonable.py
│   ├── alerta.py
│   ├── areas_gestion1.py
│   ├── areas_gestion.py
│   ├── asistencia.py
│   ├── citacion_acudiente.py
│   ├── clase_estudiante.py
│   ├── clase.py
│   ├── colegio.py
│   ├── competencia_contribucion.py
│   ├── CompetenciaDocente.py
│   ├── CompetenciaEstudiante.py
│   ├── configuracion_disciplinaria.py
│   ├── configuracion_escalamiento.py
│   ├── contribucion.py
│   ├── coordinador.py
│   ├── criterio_evaluacion.py
│   ├── descargo_estudiante.py
│   ├── docente_area.py
│   ├── docente.py
│   ├── escala_evaluacion.py
│   ├── estudiante1.py
│   ├── estudiante_acudiente.py
│   ├── estudiante.py
│   ├── evaluacion_criterio.py
│   ├── evaluacion_estudiante.py
│   ├── evaluacion_final.py
│   ├── evidencia.py
│   ├── examen1.py
│   ├── examen.py
│   ├── grupo1.py
│   ├── grupo_materia.py
│   ├── grupo.py
│   ├── indicador_logro.py
│   ├── ingreso_colegio.py
│   ├── __init__.py
│   ├── jornada_bloque.py
│   ├── jornada.py
│   ├── justificacion_acudiente.py
│   ├── materia.py
│   ├── nivel_materia.py
│   ├── notification_log.py
│   ├── novedad.py
│   ├── periodo_academico.py
│   ├── periodo.py
│   ├── permiso.py
│   ├── piar.py
│   ├── plan_estudios.py
│   ├── pregunta.py
│   ├── respuesta_novedad.py
│   ├── respuestas_examen_detalle.py
│   ├── resultado_examen.py
│   ├── sede.py
│   ├── seguimiento.py
│   ├── suscripcion.py
│   ├── tipo_examen1.py
│   ├── tipo_examen.py
│   ├── token_activacion.py
│   └── usuario.py
├── routes
│   ├── acudiente.py
│   ├── admin_routes.py
│   ├── api_acudiente.py
│   ├── api_examen_bp.py
│   ├── auth_routes.py
│   ├── auth_service.py
│   ├── colegio_routes.py
│   ├── coordinador_routes.py
│   ├── docente_routes.py
│   ├── docs_routes.py
│   ├── estudiantes_routes1.bak
│   ├── estudiantes_routes.py
│   ├── examen_routes1.py.bak
│   ├── examen_routes.py
│   ├── __init__.py
│   └── permiso_routes.py
├── services
│   ├── acudiente_service.py
│   ├── auth_service.py
│   ├── email_service1.py
│   ├── email_service.py
│   ├── estudiante_service.py
│   ├── examen_service.py
│   ├── __init__.py
│   ├── notification_service.py
│   ├── notification_worker1.py
│   └── notification_worker.py
├── templates
│   ├── acudientes
│   ├── admin
│   ├── auth
│   ├── base.html
│   ├── colegio
│   ├── coordinador
│   ├── docentes
│   ├── docs
│   ├── estudiantes
│   ├── permisos
│   └── reset_password.html
└── utils
    └── password_validator.py

16 directories, 96 files
(.venv) jorge@jorge-Latitude-7430:~/PycharmProjects/SistPROF$ ls -1 app/models/*.py | grep -v __pycache__
app/models/acudiente.py
app/models/acuerdo_correctivo.py
app/models/acuerdo_evaluacion.py
app/models/ajuste_razonable.py
app/models/alerta.py
app/models/areas_gestion1.py
app/models/areas_gestion.py
app/models/asistencia.py
app/models/citacion_acudiente.py
app/models/clase_estudiante.py
app/models/clase.py
app/models/colegio.py
app/models/competencia_contribucion.py
app/models/CompetenciaDocente.py
app/models/CompetenciaEstudiante.py
app/models/configuracion_disciplinaria.py
app/models/configuracion_escalamiento.py
app/models/contribucion.py
app/models/coordinador.py
app/models/criterio_evaluacion.py
app/models/descargo_estudiante.py
app/models/docente_area.py
app/models/docente.py
app/models/escala_evaluacion.py
app/models/estudiante1.py
app/models/estudiante_acudiente.py
app/models/estudiante.py
app/models/evaluacion_criterio.py
app/models/evaluacion_estudiante.py
app/models/evaluacion_final.py
app/models/evidencia.py
app/models/examen1.py
app/models/examen.py
app/models/grupo1.py
app/models/grupo_materia.py
app/models/grupo.py
app/models/indicador_logro.py
app/models/ingreso_colegio.py
app/models/__init__.py
app/models/jornada_bloque.py
app/models/jornada.py
app/models/justificacion_acudiente.py
app/models/materia.py
app/models/nivel_materia.py
app/models/notification_log.py
app/models/novedad.py
app/models/periodo_academico.py
app/models/periodo.py
app/models/permiso.py
app/models/piar.py
app/models/plan_estudios.py
app/models/pregunta.py
app/models/respuesta_novedad.py
app/models/respuestas_examen_detalle.py
app/models/resultado_examen.py
app/models/sede.py
app/models/seguimiento.py
app/models/suscripcion.py
app/models/tipo_examen1.py
app/models/tipo_examen.py
app/models/token_activacion.py
app/models/usuario.py
(.venv) jorge@jorge-Latitude-7430:~/PycharmProjects/SistPROF$ find app/templates -type d | head -30
app/templates
app/templates/estudiantes
app/templates/estudiantes/.idea
app/templates/estudiantes/.idea/inspectionProfiles
app/templates/auth
app/templates/docs
app/templates/permisos
app/templates/admin
app/templates/colegio
app/templates/docentes
app/templates/acudientes
app/templates/acudientes/.idea
app/templates/acudientes/.idea/inspectionProfiles
app/templates/coordinador
(.venv) jorge@jorge-Latitude-7430:~/PycharmProjects/SistPROF$ 
