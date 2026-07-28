
# Estructura de árbol completa (si tienes tree instalado)
tree -I '__pycache__|*.pyc|.git|.idea|venv|env' -L 5


├── 0:
├── app
│   ├── extensions.py
│   ├── __init__.py
│   ├── middleware
│   │   ├── auth_middleware.py
│   │   ├── __init__.py
│   │   ├── membresia_middleware.py
│   │   └── superuser_middleware.py
│   ├── models
│   │   ├── acudiente1.py
│   │   ├── acudiente.py
│   │   ├── acuerdo_correctivo.py
│   │   ├── acuerdo_evaluacion.py
│   │   ├── ajuste_razonable.py
│   │   ├── alerta.py
│   │   ├── areas_gestion1.py
│   │   ├── areas_gestion.py
│   │   ├── asistencia.py
│   │   ├── citacion_acudiente.py
│   │   ├── clase_estudiante.py
│   │   ├── clase.py
│   │   ├── colegio.py
│   │   ├── competencia_contribucion.py
│   │   ├── CompetenciaDocente.py
│   │   ├── CompetenciaEstudiante.py
│   │   ├── configuracion_disciplinaria.py
│   │   ├── configuracion_escalamiento.py
│   │   ├── contribucion.py
│   │   ├── coordinador.py
│   │   ├── criterio_evaluacion.py
│   │   ├── descargo_estudiante.py
│   │   ├── docente_area.py
│   │   ├── docente.py
│   │   ├── escala_evaluacion.py
│   │   ├── estudiante1.py
│   │   ├── estudiante_acudiente.py
│   │   ├── estudiante.py
│   │   ├── evaluacion_criterio.py
│   │   ├── evaluacion_estudiante.py
│   │   ├── evaluacion_final.py
│   │   ├── evidencia.py
│   │   ├── examen1.py
│   │   ├── examen.py
│   │   ├── grupo1.py
│   │   ├── grupo_materia.py
│   │   ├── grupo.py
│   │   ├── indicador_logro.py
│   │   ├── ingreso_colegio.py
│   │   ├── __init__.py
│   │   ├── jornada_bloque.py
│   │   ├── jornada.py
│   │   ├── justificacion_acudiente.py
│   │   ├── materia.py
│   │   ├── membresia.py
│   │   ├── nivel_materia.py
│   │   ├── notification_log.py
│   │   ├── novedad.py
│   │   ├── periodo_academico.py
│   │   ├── periodo.py
│   │   ├── permiso.py
│   │   ├── piar.py
│   │   ├── plan_estudios.py
│   │   ├── pregunta.py
│   │   ├── respuesta_novedad.py
│   │   ├── respuestas_examen_detalle.py
│   │   ├── resultado_examen.py
│   │   ├── sede.py
│   │   ├── seguimiento.py
│   │   ├── suscripcion.py
│   │   ├── tipo_examen1.py
│   │   ├── tipo_examen.py
│   │   ├── token_activacion.py
│   │   └── usuario.py
│   ├── routes
│   │   ├── acudiente.py
│   │   ├── admin_routes1.py
│   │   ├── admin_routes.py
│   │   ├── api_acudiente.py
│   │   ├── api_examen_bp.py
│   │   ├── auth_routes.py
│   │   ├── auth_service.py
│   │   ├── colegio_routes.py
│   │   ├── coordinador_routes.py
│   │   ├── docente_routes.py
│   │   ├── docs_routes.py
│   │   ├── estudiantes_routes1.py
│   │   ├── estudiantes_routes.py
│   │   ├── examen_routes1.py.bak
│   │   ├── examen_routes.py
│   │   ├── __init__.py
│   │   ├── membresia_routes.py
│   │   └── permiso_routes.py
│   ├── services
│   │   ├── acudiente_service.py
│   │   ├── auth_service1.py
│   │   ├── auth_service.py
│   │   ├── document_service.py
│   │   ├── email_service1.py
│   │   ├── email_service.py
│   │   ├── estudiante_service.py
│   │   ├── examen_service.py
│   │   ├── ia_service1.py
│   │   ├── ia_service.py
│   │   ├── __init__.py
│   │   ├── notification_service.py
│   │   ├── notification_worker1.py
│   │   └── notification_worker.py
│   ├── templates
│   │   ├── acudientes
│   │   │   ├── acudiente_base1.html
│   │   │   ├── acudiente_base.html
│   │   │   ├── acudientes.html
│   │   │   ├── dashboard_acudiente.html
│   │   │   ├── estudiante_detalle.html
│   │   │   ├── formulario_acudiente1.html
│   │   │   ├── formulario_acudiente.html
│   │   │   └── mis_estudiantes.html
│   │   ├── admin
│   │   │   ├── admin_base.html
│   │   │   ├── dashboard.html
│   │   │   ├── detalle_colegio.html
│   │   │   ├── estadisticas.html
│   │   │   ├── usuario_detalle.html
│   │   │   └── usuarios.html
│   │   ├── auth
│   │   │   ├── estado_cuenta.html
│   │   │   ├── forgot_password.html
│   │   │   ├── login.html
│   │   │   ├── register1.html
│   │   │   ├── register.html
│   │   │   └── reset_password.html
│   │   ├── base.html
│   │   ├── colegio
│   │   │   ├── areas.html
│   │   │   ├── asignar_materias.html
│   │   │   ├── carga_academica.html
│   │   │   ├── colegio_base1.html
│   │   │   ├── colegio_base.html
│   │   │   ├── configuracion_disciplina.html
│   │   │   ├── configuracion_escalamiento.html
│   │   │   ├── configurar_bloques.html
│   │   │   ├── configurar_materias_nivel.html
│   │   │   ├── dashboard1.html
│   │   │   ├── dashboard.html
│   │   │   ├── detalle_sede1.html
│   │   │   ├── detalle_sede.html
│   │   │   ├── dividir_grupo.html
│   │   │   ├── docentes.html
│   │   │   ├── formulario_area.html
│   │   │   ├── formulario_docente.html
│   │   │   ├── formulario_grupo.html
│   │   │   ├── formulario_jornada.html
│   │   │   ├── formulario_materia.html
│   │   │   ├── formulario_permiso.html
│   │   │   ├── formulario_sede1.html
│   │   │   ├── formulario_sede.html
│   │   │   ├── fusionar_grupo.html
│   │   │   ├── grupos1.html
│   │   │   ├── grupos.html
│   │   │   ├── horario_grupo.html
│   │   │   ├── jornadas_sede.html
│   │   │   ├── materias.html
│   │   │   ├── mi_colegio.html
│   │   │   ├── permisos_docente.html
│   │   │   ├── permisos.html
│   │   │   ├── plan_estudios1.html
│   │   │   ├── plan_estudios.html
│   │   │   ├── redistribuir_estudiantes.html
│   │   │   ├── resumen_carga_academica.html
│   │   │   ├── sedes1.html
│   │   │   └── sedes.html
│   │   ├── coordinador
│   │   │   ├── cambiar_password1.html
│   │   │   ├── cambiar_password.html
│   │   │   ├── coordinador_base1.html
│   │   │   ├── coordinador_base.html
│   │   │   ├── coordinador_dashboard.html
│   │   │   ├── coordinadores1.html
│   │   │   ├── coordinadores.html
│   │   │   ├── docentes.html
│   │   │   ├── editar_coordinador1.1.html
│   │   │   ├── editar_coordinador1.html
│   │   │   ├── editar_coordinador.html
│   │   │   ├── estudiantes.html
│   │   │   ├── formulario_coordinador1.html
│   │   │   ├── formulario_coordinador.html
│   │   │   ├── permisos.html
│   │   │   └── sedes.html
│   │   ├── docentes
│   │   │   ├── cambiar_password.html
│   │   │   ├── citaciones.html
│   │   │   ├── dashboard1.html
│   │   │   ├── dashboard.html
│   │   │   ├── detalle.html
│   │   │   ├── docente_base1.html
│   │   │   ├── docente_base.html
│   │   │   ├── estudiantes.html
│   │   │   ├── formulario1.html
│   │   │   ├── formulario.html
│   │   │   ├── listado.html
│   │   │   ├── nuevo_permiso.html
│   │   │   ├── observador.html
│   │   │   ├── perfil.html
│   │   │   ├── permisos.html
│   │   │   └── seguimiento.html
│   │   ├── docs
│   │   │   ├── doc.html
│   │   │   ├── docs.html
│   │   │   └── index.html
│   │   ├── estudiantes
│   │   │   ├── dashboard_estudiante1.html
│   │   │   ├── dashboard_estudiante.html
│   │   │   ├── detalle.html
│   │   │   ├── estudiante1.html
│   │   │   ├── estudiante_base1.html
│   │   │   ├── estudiante_base.html
│   │   │   ├── estudiante.html
│   │   │   ├── examenes_disponibles.html
│   │   │   ├── examen_estudiante.html
│   │   │   ├── formulario1.html
│   │   │   ├── formulario.html
│   │   │   ├── ingenios.html
│   │   │   ├── Listado1.html
│   │   │   ├── listado_estudiantes.html
│   │   │   ├── listado_examenes.html
│   │   │   ├── listado.html
│   │   │   └── mis_resultado.html
│   │   ├── examenes
│   │   │   ├── crear_examen_ia.html
│   │   │   ├── editar_examen.html
│   │   │   ├── listar_examenes.html
│   │   │   ├── preview_ia.html
│   │   │   ├── ver_examen1.html
│   │   │   └── ver_examen.html
│   │   ├── membresia
│   │   │   ├── gestionar_membresias.html
│   │   │   ├── mi_plan.html
│   │   │   └── renovar.html
│   │   ├── permisos
│   │   │   ├── editar.html
│   │   │   ├── formulario.html
│   │   │   ├── listado.html
│   │   │   └── permisos_form.html
│   │   └── reset_password.html
│   └── utils
│       └── password_validator.py
├── conexion.py
├── config1.py
├── config.py
├── docs
│   ├── 0_General_SistPROF.md
│   ├── 1_Académica_SistPROF.md
│   ├── 2_Modulo_Aademinco.md
│   ├── 3_Evaluación_SistPROF.md
│   ├── 4_Modelo_Datos_SistPROF.md
│   ├── 6_Acudientes_SistPROF.md
│   ├── Activar_usuarios.md
│   ├── arquitectura_bd(1).png
│   ├── arquitectura_bd.png
│   ├── arquitectura_CistPROF.png
│   ├── arquitectura.md
│   ├── arquitecturapng.md
│   ├── base_datos_diagrama.md
│   ├── bruchere.md
│   ├── bruchure
│   │   ├── beneficios_institucion.png
│   │   ├── control_asistencia.png
│   │   ├── evaluacion_docente.png
│   │   ├── gestion_academica.png
│   │   ├── gestion_disciplinaira.png
│   │   ├── implementacion.png
│   │   ├── inclusion_educativa.png
│   │   ├── modalidad_servicio.png
│   │   ├── natillera.png
│   │   ├── permisos_docentes.png
│   │   ├── piar.png
│   │   └── presentacion.png
│   ├── ChatGPT Image 27 abr 2026, 06_08_13 p.m..png
│   ├── ChatGPT Image 27 abr 2026, 06_08_55 p.m..png
│   ├── DDL.md
│   ├── Docente.md
│   ├── Dsc-SisPROF.md
│   ├── estructuraBD.md
│   ├── estructura.md
│   ├── EvaluaconDOC-EST.md
│   ├── Integracion.md
│   ├── Migracion.md
│   ├── models.md
│   ├── Módulo de Exámenes SistPROF.md
│   ├── Modulo_Administrativo.md
│   ├── Pendiente.md
│   ├── SistPROF.md
│   ├── SistPROF.MD
│   ├── superadmin.md
│   └── Tree.md
├── ejecutar.py
├── fly.toml
├── ión delta usando hasta 12 hilos
├── listar_modelos.py
├── migrations
│   ├── alembic.ini
│   ├── env.py
│   ├── README
│   ├── script.py.mako
│   └── versions
│       ├── 36a3c839603b_estructura_inicial.py
│       └── 48daffe3eec0_estructura_completa_supabase.py
├── presentacion.html
├── Procfile
├── requirements.txt
├── reset_passwordJES.py
├── run.py
├── runtime.txt
├── static
│   ├── css
│   │   ├── admin.css
│   │   ├── auth1.css
│   │   ├── auth.css
│   │   ├── colegio1.css
│   │   ├── colegio.css
│   │   ├── coordinador.css
│   │   ├── docentes.css
│   │   ├── examen_estilos.css
│   │   ├── main.css
│   │   └── permisos.css
│   ├── examenes
│   ├── __init__.py
│   └── js
│       ├── ClsEstudiante.js
│       ├── CslTingenios_Estudiante.js
│       ├── formulario-permiso.js
│       ├── main.js
│       ├── T-IngeniosB1GC2025_09B.js
│       └── T-IngeniosB1GC2025_09.js
├── test_gemini.py
├── textModelosIA.py
└── wsgi.py

