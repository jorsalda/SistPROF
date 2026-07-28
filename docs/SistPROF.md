# 📚 Documentación Completa de SistPROF

---

## 🏫 Documento 1: Arquitectura Administrativa

### Objetivo
Definir la estructura organizacional y administrativa de SistPROF como plataforma SaaS multiinstitucional.

### 🏢 Multi-Tenencia Institucional

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| SistPROF será una plataforma SaaS multiinstitución. | Un único sistema debe administrar múltiples colegios de forma aislada. | `colegios`, `colegio_id` en todas las tablas |
| Cada colegio tendrá autonomía operativa completa. | Las instituciones tienen procesos, configuraciones y normativas diferentes. | Todas las tablas con `colegio_id` como filtro |
| Cada colegio tendrá un código de acceso único. | Permite identificación rápida y procesos de registro simplificados. | `colegios.codigo_acceso` (único) |
| Los colegios tendrán período de prueba configurable. | Facilita la conversión de clientes potenciales. | `colegios.en_prueba`, `colegios.dias_prueba` |
| Existirá control de expiración de cuentas. | Garantiza modelo de negocio basado en suscripciones. | `colegios.fecha_expiracion`, `suscripciones` |
| La información histórica nunca se elimina físicamente. | Garantiza trazabilidad institucional y cumplimiento legal. | Campos `activo` en todas las entidades |
| Cada colegio podrá tener múltiples sedes. | Muchos colegios operan desde varias ubicaciones físicas. | `sedes` con FK a `colegios` |
| Las sedes tendrán configuración independiente. | Cada sede puede tener horarios y capacidades diferentes. | `jornadas_colegio`, `grupos` vinculados a sede |

### 👥 Gestión de Usuarios y Roles

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| La autenticación será centralizada en una sola tabla. | Un único mecanismo de acceso para toda la plataforma. | `usuarios` como tabla maestra |
| Usuarios y personas serán entidades separadas. | Una persona puede requerir autenticación independiente de sus datos funcionales. | `usuarios`, `docentes`, `estudiantes`, `acudientes`, `coordinadores` |
| El sistema manejará 6 roles institucionales definidos. | Permite control granular de accesos según responsabilidades. | `usuarios.rol` (ENUM: superadmin, admin_colegio, docente, estudiante, acudiente, coordinador) |
| Existirá un rol de superadministrador global. | Administración transversal de la plataforma sin restricciones institucionales. | `usuarios.is_superadmin` |
| Se implementará protección contra accesos indebidos. | Incrementar seguridad y prevenir ataques de fuerza bruta. | `usuarios.failed_attempts`, `usuarios.locked_until` |
| Los usuarios requerirán aprobación para activarse. | Control administrativo sobre quién accede al sistema. | `usuarios.is_approved`, `usuarios.fecha_aprobacion` |
| Se implementará sistema de tokens de activación. | Proceso seguro de activación de cuentas vía email. | `tokens_activacion` con expiración |
| Los usuarios tendrán asociación a sede específica. | Control de acceso basado en ubicación física. | `usuarios.sede_id` |

### 🔐 Seguridad y Autenticación

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las contraseñas se almacenarán hasheadas. | Seguridad básica contra exposición de credenciales. | `usuarios.password_hash` (256 chars) |
| Existirá middleware de autenticación. | Protección transversal de todas las rutas. | `middleware/auth_middleware.py` |
| Existirá middleware de superusuario. | Control adicional para operaciones críticas. | `middleware/superuser_middleware.py` |
| Los tokens de activación tendrán expiración. | Prevención de uso indebido de tokens antiguos. | `tokens_activacion.fecha_expiracion` |
| Los tokens serán de un solo uso. | Garantiza que no puedan reutilizarse. | `tokens_activacion.usado` |
| Se validará fortaleza de contraseñas. | Cumplimiento de políticas de seguridad. | `utils/password_validator.py` |
| Existirá recuperación de contraseña por email. | Experiencia de usuario y accesibilidad. | `templates/reset_password.html` |
| Se registrará fecha de aprobación de usuarios. | Auditoría y control administrativo. | `usuarios.fecha_aprobacion` |

### 💼 Suscripciones y Monetización

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada colegio tendrá una suscripción activa. | Modelo de negocio basado en suscripciones. | `suscripciones` con FK única a `colegios` |
| Las suscripciones tendrán período de prueba. | Facilita adopción y evaluación del sistema. | `suscripciones.en_prueba` |
| Existirá límite de sedes por suscripción. | Modelo de precios escalonado. | `suscripciones.limite_sedes` |
| Se registrará precio base de suscripción. | Base para facturación y reportes financieros. | `suscripciones.precio_base` |
| Las suscripciones tendrán fecha de expiración. | Control automático de acceso. | `suscripciones.fecha_fin` |
| Se podrá renovar o cancelar suscripciones. | Flexibilidad comercial. | `suscripciones.activo` |

### 📧 Sistema de Notificaciones

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirá un sistema centralizado de notificaciones. | Consistencia en comunicación con usuarios. | `services/notification_service.py` |
| Se usará procesamiento asíncrono de notificaciones. | No bloquear la aplicación principal. | `services/notification_worker.py` |
| Se registrará log de todas las notificaciones. | Trazabilidad y debugging. | `notification_logs` |
| Se soportarán múltiples tipos de notificación. | Flexibilidad para diferentes casos de uso. | `notification_logs.tipo` (ENUM: password_reset, citacion_acudiente, activacion_cuenta, alerta_sistema, ingreso_qr) |
| Se integrará con proveedor externo de email. | Infraestructura profesional de envío. | `notification_logs.proveedor` (default: 'resend') |
| Se registrará estado de cada notificación. | Control de entrega y reintentos. | `notification_logs.estado` (pendiente, enviado, rebotado, fallido) |
| Se almacenará payload completo en JSON. | Auditoría completa del contenido enviado. | `notification_logs.payload_json` |

---

## 🎓 Documento 2: Arquitectura Académica

### Objetivo
Definir la estructura académica que soporta la gestión de materias, grupos, clases y períodos.

### 📚 Gestión de Materias y Plan de Estudios

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las materias serán entidades independientes. | Catálogo reutilizable entre colegios. | `materias` con `nombre` y `nivel_educativo` |
| Las materias tendrán nivel educativo asociado. | Clasificación por niveles (básica, media, etc.). | `materias.nivel_educativo` |
| Existirá plan de estudios por colegio y grado. | Cada institución define su malla curricular. | `plan_estudios` con `colegio_id`, `grado`, `materia_id` |
| El plan de estudios incluirá horas semanales. | Control de intensidad horaria. | `plan_estudios.horas_semanales` |
| Las materias tendrán competencias asociadas. | Estructura curricular basada en competencias. | `competencias_materia` |
| Las competencias tendrán porcentaje asignable. | Ponderación flexible por competencia. | `competencias_materia.porcentaje` |
| Existirán indicadores de logro por competencia. | Evidencias objetivas de aprendizaje. | `indicadores_logro` con FK a `competencias_materia` |
| Las materias tendrán niveles por nivel educativo. | Progresión curricular estructurada. | `nivel_materia` con `nivel_educativo` y `materia_id` |

### 🏫 Organización de Grupos

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los grupos se organizarán por año lectivo. | Control histórico de promociones. | `grupos.anio_lectivo` |
| Cada grupo tendrá grado, nombre y capacidad. | Estructura estándar de organización estudiantil. | `grupos.grado`, `grupos.nombre`, `grupos.capacidad_maxima` |
| Los grupos se vincularán a sede y jornada. | Organización física y temporal. | `grupos.sede_id`, `grupos.jornada_id` |
| Cada grupo tendrá un director asignado. | Responsable académico del grupo. | `grupos.director_docente_id` con FK a `docentes` |
| Existirá historial de directores de grupo. | Trazabilidad de cambios de director. | `directores_grupo` con `fecha_inicio`, `fecha_fin` |
| Solo habrá un director activo por grupo. | Evita conflictos de responsabilidad. | Índice único `director_grupo_activo_unico` WHERE `activo = true` |
| Los grupos tendrán materias asignadas. | Definición de currículo por grupo. | `grupo_materias` con `grupo_id`, `materia_id`, `docente_id` |
| Se registrarán horas semanales por materia-grupo. | Control de intensidad horaria real. | `grupo_materias.horas_semanales` |

### 📅 Gestión de Períodos Académicos

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirán períodos académicos por colegio. | Cada institución define su calendario. | `periodos_academicos` con `colegio_id` |
| Los períodos tendrán fechas de inicio y fin. | Control de vigencia temporal. | `periodos_academicos.fecha_inicio`, `periodos_academicos.fecha_fin` |
| Se definirá orden de períodos en el año. | Secuencia lógica de períodos. | `periodos_academicos.orden` |
| Existirá un período final por colegio-año. | Marcador de cierre académico. | `periodos_academicos.es_final` |
| Los períodos podrán activarse/desactivarse. | Control administrativo de períodos vigentes. | `periodos_academicos.activo` |
| Se soportarán períodos generales del sistema. | Configuración global de año lectivo. | `periodos` con `anio_lectivo` |

### ⏰ Jornadas y Horarios

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada colegio definirá sus jornadas. | Flexibilidad horaria institucional. | `jornadas_colegio` con `colegio_id` |
| Las jornadas tendrán hora inicio y fin. | Control de horario escolar. | `jornadas_colegio.hora_inicio`, `jornadas_colegio.hora_fin` |
| Se permitirá tolerancia en horarios. | Flexibilidad para llegadas tardías. | `jornadas_colegio.tolerancia_minutos` |
| Las jornadas se vincularán a sede específica. | Horarios por ubicación física. | `jornadas_colegio.sede_id` |
| Existirán bloques dentro de cada jornada. | Definición de recreos, almuerzos, etc. | `jornada_bloques` con `jornada_id` |
| Los bloques tendrán tipo y nombre. | Clasificación de bloques (recreo, clase, etc.). | `jornada_bloques.tipo`, `jornada_bloques.nombre` |
| Los bloques tendrán orden secuencial. | Estructura temporal ordenada. | `jornada_bloques.orden` |
| Se validará que hora inicio < hora fin. | Integridad de datos horaria. | CONSTRAINT `chk_horario_valido` |

### 👨‍🏫 Gestión de Docentes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los docentes tendrán datos personales completos. | Información de contacto y identificación. | `docentes.nombre`, `docentes.documento`, `docentes.telefono`, `docentes.email` |
| Cada docente se vinculará a colegio y sede. | Asignación institucional. | `docentes.colegio_id`, `docentes.sede_id` |
| Los docentes tendrán usuario de sistema asociado. | Acceso a la plataforma. | `docentes.usuario_id` con FK a `usuarios` |
| Los docentes tendrán áreas de enseñanza. | Especialización por áreas. | `docente_areas` con `docente_id`, `area_id` |
| Los docentes podrán tener permisos académicos. | Control de ausencias y reemplazos. | `permisos` con `docente_id`, `fecha_inicio`, `fecha_fin` |
| Los permisos tendrán tipo y observación. | Clasificación de permisos. | `permisos.tipo`, `permisos.observacion` |
| Se validará que fecha_fin >= fecha_inicio. | Integridad temporal. | CONSTRAINT `chk_permiso_fechas` |

### 👨‍🎓 Gestión de Estudiantes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los estudiantes tendrán datos completos de contacto. | Información esencial para comunicación. | `estudiantes.nombre`, `estudiantes.apellido`, `estudiantes.documento`, `estudiantes.telefono`, `estudiantes.email`, `estudiantes.direccion` |
| Cada estudiante se vinculará a colegio, sede y jornada. | Organización institucional completa. | `estudiantes.colegio_id`, `estudiantes.sede_id`, `estudiantes.jornada_id` |
| Los estudiantes tendrán grupo asignado. | Organización académica. | `estudiantes.grupo_id` con FK a `grupos` |
| Cada estudiante tendrá acudiente principal. | Contacto de emergencia y responsabilidad. | `estudiantes.acudiente_principal_id` con FK a `acudientes` |
| Existirá relación muchos-a-muchos con acudientes. | Soporte para múltiples acudientes por estudiante. | `estudiante_acudiente` (tabla intermedia) |
| Los estudiantes tendrán token QR único. | Control de ingreso al colegio. | `estudiantes.qr_token` (único) |
| Los estudiantes tendrán usuario de sistema opcional. | Acceso a plataforma para consultas. | `estudiantes.usuario_id` con FK a `usuarios` |
| Se validará unicidad de documento y email. | Prevención de duplicados. | CONSTRAINTS `estudiantes_documento_key`, `estudiantes_email_key` |

### 👪 Gestión de Acudientes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los acudientes tendrán datos de contacto completos. | Comunicación efectiva con familia. | `acudientes.nombre`, `acudientes.telefono`, `acudientes.email`, `acudientes.direccion` |
| Se registrará parentesco con el estudiante. | Información de relación familiar. | `acudientes.parentesco` |
| Los acudientes tendrán usuario de sistema. | Acceso a plataforma para consultas. | `acudientes.usuario_id` con FK a `usuarios` |
| Los acudientes se vincularán a colegio. | Pertenencia institucional. | `acudientes.colegio_id` con FK a `colegios` |
| Se validará unicidad de email. | Prevención de duplicados. | CONSTRAINT `acudientes_email_key` |

### 👔 Gestión de Coordinadores

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los coordinadores tendrán usuario de sistema. | Acceso a plataforma con privilegios. | `coordinadores.usuario_id` con FK a `usuarios` |
| Los coordinadores se vincularán a colegio y sede. | Asignación institucional. | `coordinadores.colegio_id`, `coordinadores.sede_id` |
| Se registrará cargo del coordinador. | Identificación de rol específico. | `coordinadores.cargo` |
| Los coordinadores tendrán datos de contacto. | Comunicación institucional. | `coordinadores.documento`, `coordinadores.telefono` |

### 📋 Asignación de Clases

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las clases tendrán docente, materia y grupo. | Asignación académica completa. | `clases.docente_id`, `clases.materia_id`, `clases.grupo_id` |
| Las clases tendrán día y horario definido. | Estructura temporal de enseñanza. | `clases.dia` (ENUM), `clases.hora_inicio`, `clases.hora_fin` |
| Se validará que no haya conflictos de horario. | Prevención de sobreposición de clases. | CONSTRAINT `horario_unico` UNIQUE(docente_id, dia, hora_inicio, hora_fin) |
| Las clases se vincularán a grupo-materia. | Referencia a asignación curricular. | `clases.grupo_materia_id` con FK a `grupo_materias` |
| Existirá tabla de estudiantes por clase. | Matriculación explícita. | `clase_estudiantes` con `clase_id`, `estudiante_id` |
| Se validará unicidad de matrícula. | Prevención de duplicados. | CONSTRAINT `unica_matricula` UNIQUE(clase_id, estudiante_id) |

### 📊 Asistencia y Control

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Se registrará asistencia por clase y fecha. | Control diario de asistencia. | `asistencias` con `clase_id`, `estudiante_id`, `fecha` |
| La asistencia tendrá estado y observación. | Detalle de situación del estudiante. | `asistencias.estado`, `asistencias.observacion` |
| Se registrará quién toma la asistencia. | Auditoría y responsabilidad. | `asistencias.registrada_por` con FK a `usuarios` |
| Se validará unicidad de asistencia por clase-fecha. | Prevención de duplicados. | CONSTRAINT `unica_asistencia_por_clase` UNIQUE(estudiante_id, clase_id, fecha) |
| Existirá control de ingreso/salida con QR. | Seguridad y registro de movimientos. | `ingresos_colegio` con `estudiante_id`, `qr_token` |
| Los ingresos tendrán tipo de evento. | Clasificación de movimientos. | `ingresos_colegio.tipo_evento` (ENUM: ingreso, salida) |
| Se validará un evento por tipo por día. | Prevención de duplicados diarios. | UNIQUE INDEX `unico_evento_por_dia` (estudiante_id, fecha, tipo_evento) |

---

## 📊 Documento 3: Arquitectura de Evaluación

### Objetivo
Definir el modelo de evaluación basado en competencias, con escalas configurables y automatización de cálculos.

### 🎯 Modelo de Competencias

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| La evaluación estará basada en competencias. | Permite seguimiento real del aprendizaje. | `competencias`, `competencias_materia`, `competencias_periodo` |
| Las competencias pertenecerán a áreas de gestión. | Estructura jerárquica del currículo. | `competencias.area_id` con FK a `areas_gestion` |
| Las áreas de gestión tendrán porcentaje asignado. | Ponderación por área. | `areas_gestion.porcentaje` |
| Las competencias tendrán orden dentro del área. | Estructura secuencial. | `competencias.orden` |
| Se validará unicidad de competencia por área. | Prevención de duplicados. | CONSTRAINT `unica_competencia_por_area` UNIQUE(area_id, nombre) |
| Se validará unicidad de orden por área. | Secuencia lógica. | CONSTRAINT `unico_orden_por_area` UNIQUE(area_id, orden) |
| Existirán competencias específicas por período. | Planeación temporal. | `competencias_periodo` con `colegio_id`, `periodo_id`, `materia_id`, `grado` |
| Las competencias por período tendrán porcentaje. | Ponderación flexible. | `competencias_periodo.porcentaje` |

### 📈 Contribuciones y Criterios

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las competencias tendrán contribuciones. | Desglose de elementos evaluables. | `contribuciones` con `competencia_id` |
| Las contribuciones tendrán orden secuencial. | Estructura lógica. | `contribuciones.orden` |
| Se validará unicidad de orden por competencia. | Secuencia lógica. | CONSTRAINT `unico_orden_por_competencia` UNIQUE(competencia_id, orden) |
| Los acuerdos de evaluación definirán criterios. | Especificación de qué se evalúa. | `criterios_evaluacion` con `acuerdo_id`, `contribucion_id` |
| Los criterios tendrán descripción detallada. | Claridad en expectativas. | `criterios_evaluacion.descripcion` |
| Se bloquearán criterios de acuerdos cerrados. | Integridad de evaluación finalizada. | TRIGGER `trg_bloquear_criterios_si_cerrado` |

### 📝 Acuerdos de Evaluación

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada docente tendrá acuerdo de evaluación por año. | Formalización de planeación. | `acuerdos_evaluacion` con `docente_id`, `anio` |
| Los acuerdos tendrán estado de_workflow. | Control de proceso. | `acuerdos_evaluacion.estado` (BORRADOR, CERRADO) |
| Se validará unicidad de acuerdo por docente-año. | Prevención de duplicados. | CONSTRAINT `unico_docente_anio` UNIQUE(docente_id, anio) |
| Los acuerdos se vincularán a colegio. | Pertenencia institucional. | `acuerdos_evaluacion.colegio_id` |
| Existirá evaluación final por acuerdo. | Cierre de proceso evaluativo. | `evaluacion_final` con `acuerdo_id` |
| La evaluación final tendrá estado. | Control de cierre. | `evaluacion_final.estado` (ABIERTO, CERRADO) |
| Se registrarán observaciones finales. | Retroalimentación cualitativa. | `evaluacion_final.observaciones_finales` |

### 📊 Escalas de Evaluación

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada colegio definirá su propia escala de evaluación. | Adaptación a diferentes SIEE institucionales. | `escala_evaluacion` con `colegio_id` |
| La escala tendrá nombre descriptivo. | Identificación clara. | `escala_evaluacion.nombre` |
| La escala tendrá rango mínimo y máximo. | Definición de límites. | `escala_evaluacion.nota_min`, `escala_evaluacion.nota_max` |
| Se soportará tipo de escala numérica. | Evaluación cuantitativa. | `escala_evaluacion.tipo_escala` = 'NUMERICA' |
| Se soportará tipo de escala cualitativa. | Evaluación por desempeños. | `escala_evaluacion.tipo_escala` = 'CUALITATIVA' |
| Existirá configuración de evaluación por colegio. | Parametrización institucional. | `configuracion_evaluacion` con `colegio_id` |
| La configuración definirá tipo de captura. | Flexibilidad de entrada de datos. | `configuracion_evaluacion.tipo_captura` (NUMERICA, CUALITATIVA, MIXTA) |
| La configuración definirá qué mostrar en boletín. | Control de presentación. | `configuracion_evaluacion.mostrar_boletin` (NUMERICA, CUALITATIVA, AMBAS) |
| La configuración definirá nota mínima y máxima. | Rango de calificación. | `configuracion_evaluacion.nota_min`, `configuracion_evaluacion.nota_max` |

### 📋 Modelo de Evaluación Institucional

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada colegio definirá su propio modelo de evaluación. | Cumplimiento del SIEE institucional. | `modelo_evaluacion_estudiante` con `colegio_id` |
| Los componentes de evaluación serán parametrizables. | Evita reglas rígidas codificadas. | `modelo_evaluacion_estudiante.nombre`, `modelo_evaluacion_estudiante.porcentaje` |
| La suma de componentes debe ser 100%. | Garantiza consistencia matemática. | CONSTRAINT `chk_porcentaje_modelo` CHECK (porcentaje >= 0 AND porcentaje <= 100) |
| Los componentes tendrán orden definido. | Estructura lógica. | `modelo_evaluacion_estudiante.orden` |
| Se validará unicidad de componente por colegio. | Prevención de duplicados. | CONSTRAINT `unique_componente_colegio` UNIQUE(colegio_id, nombre) |
| Se validará unicidad de orden por colegio. | Secuencia lógica. | CONSTRAINT `unique_orden_colegio` UNIQUE(colegio_id, orden) |
| Existirán componentes de evaluación generales. | Configuración transversal. | `componentes_evaluacion` con `colegio_id`, `nombre`, `porcentaje` |

### 🎓 Evaluación de Estudiantes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Se registrarán evaluaciones por estudiante e indicador. | Seguimiento individualizado. | `evaluaciones_estudiante` con `estudiante_id`, `indicador_id`, `periodo_id` |
| Las evaluaciones tendrán calificación numérica. | Medición cuantitativa. | `evaluaciones_estudiante.calificacion` |
| Las evaluaciones tendrán observación cualitativa. | Retroalimentación descriptiva. | `evaluaciones_estudiante.observacion` |
| Se evaluarán criterios en evaluación final. | Cierre de proceso evaluativo. | `evaluacion_criterio` con `evaluacion_final_id`, `criterio_id` |
| Las calificaciones tendrán validación de rango. | Integridad de datos. | CONSTRAINT `chk_calificacion_valida` CHECK (calificacion >= 0 AND calificacion <= 5) |
| Se validará unicidad de evaluación por criterio. | Prevención de duplicados. | CONSTRAINT `unica_eval_por_criterio` UNIQUE(evaluacion_final_id, criterio_id) |
| Existirán seguimientos de acuerdos. | Retroalimentación continua. | `seguimientos` con `acuerdo_id`, `observaciones`, `recomendaciones` |

### 📄 Boletines y Reportes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los boletines serán configurables por institución. | Cada colegio tiene formatos distintos. | Módulo de boletines basado en `configuracion_evaluacion` |
| Se soportarán boletines cuantitativos. | Compatibilidad institucional. | Función `fn_boletin_estudiante` |
| Se soportarán boletines cualitativos. | Compatibilidad institucional. | Niveles: Bajo, Básico, Alto, Superior |
| Se soportarán boletines mixtos. | Mayor flexibilidad institucional. | Función `fn_boletin_estudiante_pro` |
| Los resultados se generarán automáticamente. | Reducir carga operativa. | Funciones SQL `fn_boletin_estudiante`, `fn_boletin_estudiante_pro` |
| Existirán informes detallados por área. | Desglose por áreas de gestión. | Función `fn_informe_detalle` |
| Existirán informes MEN (Ministerio Educación). | Cumplimiento normativo. | Función `fn_informe_men`, `get_informe_men` |
| Los informes calcularán promedios ponderados. | Cálculo automático de notas. | Funciones SQL con CTEs y JOINs |
| Los informes asignarán nivel de desempeño. | Clasificación automática. | CASE WHEN en funciones SQL (Bajo < 3.0, Básico < 3.9, Alto < 4.6, Superior >= 4.6) |

### 📊 Evidencias de Aprendizaje

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los criterios tendrán evidencias asociadas. | Soporte documental de evaluación. | `evidencias` con `criterio_id` |
| Las evidencias tendrán tipo y descripción. | Clasificación de evidencias. | `evidencias.tipo`, `evidencias.descripcion` |
| Las evidencias podrán tener URL de recurso. | Enlace a material de soporte. | `evidencias.url` |
| Las evidencias requerirán aprobación. | Control de calidad. | `evidencias.aprobado` |
| Las evidencias tendrán observación de admin. | Retroalimentación administrativa. | `evidencias.observacion_admin` |

---

## ⚖️ Documento 4: Arquitectura Disciplinaria

### Objetivo
Definir el sistema de gestión disciplinaria con escalamiento automático, citaciones y soporte para inclusión (PIAR).

### 📋 Gestión de Novedades

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las novedades tendrán tipo clasificado. | Categorización de eventos. | `novedades.tipo_novedad` (ENUM: DISCIPLINA, ACADEMICO, LLEGADA_TARDE) |
| Las novedades tendrán nivel de gravedad. | Clasificación de severidad. | `novedades.gravedad` (ENUM: Tipo 1, Tipo 2, Tipo 3) |
| Las novedades tendrán informe detallado. | Descripción completa del evento. | `novedades.informe` |
| Las novedades tendrán fecha y hora. | Registro temporal preciso. | `novedades.fecha`, `novedades.hora` |
| Las novedades tendrán categoría opcional. | Clasificación adicional. | `novedades.categoria` |
| Las novedades registrarán quién las reporta. | Auditoría y responsabilidad. | `novedades.registrada_por` con FK a `usuarios` |
| Las novedades se vincularán a estudiante. | Asociación con sujeto del evento. | `novedades.estudiante_id` con FK a `estudiantes` |

### 🔄 Escalamiento Automático

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirá escalamiento automático de Tipo 2 a Tipo 3. | Aplicación consistente de reglas institucionales. | TRIGGER `trg_escalamiento_tipo2` ejecuta `fn_escalamiento_tipo2_a_tipo3` |
| El escalamiento será configurable por colegio. | Flexibilidad institucional. | `configuracion_escalamiento` con `colegio_id` |
| Se podrá escalar por cantidad o por tiempo. | Diferentes políticas institucionales. | `configuracion_escalamiento.usar_tiempo` |
| Se definirá cantidad de Tipo 2 para escalar. | Umbral configurable. | `configuracion_escalamiento.cantidad_tipo2` |
| Se definirá ventana de tiempo para evaluación. | Período de análisis. | `configuracion_escalamiento.dias_evaluacion` |
| El escalamiento se ejecutará antes de insertar. | Corrección en tiempo real. | TRIGGER BEFORE INSERT |

### 📞 Citaciones Automáticas

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Se generarán citaciones automáticas a acudientes. | Respuesta inmediata a eventos críticos. | TRIGGER `trg_citacion_automatica` ejecuta `fn_generar_citacion_automatica` |
| Las citaciones Tipo 3 serán automáticas. | Protocolo para faltas graves. | Función `fn_generar_citacion_automatica` con condición `gravedad = 'Tipo 3'` |
| Las citaciones tendrán motivo detallado. | Claridad en razón de citación. | `citaciones_acudiente.motivo` |
| Las citaciones tendrán fecha programada. | Agenda de reunión. | `citaciones_acudiente.fecha_citacion` |
| Las citaciones tendrán estado de seguimiento. | Control de proceso. | `citaciones_acudiente.estado` (pendiente, asistió, no asistió, reprogramada) |
| Las citaciones tendrán tipo de origen. | Clasificación de fuente. | `citaciones_acudiente.tipo_origen` (TIPO_3, PIAR_TIPO2, PIAR_TIPO3) |
| Se validarán citaciones únicas por novedad. | Prevención de duplicados. | UNIQUE INDEX `unique_citacion_por_novedad` |
| Se validarán citaciones únicas por tipo. | Una citación por tipo por estudiante. | UNIQUE INDEX `unique_citacion_por_tipo` |

### 🎯 Sistema PIAR (Inclusión)

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirá sistema PIAR para estudiantes con necesidades especiales. | Cumplimiento de normativa de inclusión. | `piar` con `estudiante_id` |
| Los PIAR tendrán diagnóstico documentado. | Base para ajustes. | `piar.diagnostico` |
| Los PIAR tendrán objetivos definidos. | Metas de aprendizaje. | `piar.objetivos` |
| Los PIAR tendrán período de vigencia. | Control temporal. | `piar.fecha_inicio`, `piar.fecha_fin` |
| Solo habrá un PIAR activo por estudiante. | Evita conflictos. | UNIQUE INDEX `unico_piar_activo` WHERE `activo = true` |
| Los PIAR tendrán ajustes razonables. | Adaptaciones específicas. | `ajustes_razonables` con `piar_id` |
| Los ajustes razonables tendrán descripción. | Detalle de adaptación. | `ajustes_razonables.descripcion` |
| Los ajustes razonables registrarán aplicación. | Seguimiento de implementación. | `ajustes_razonables.aplicado`, `ajustes_razonables.fecha_aplicacion` |
| Se generarán citaciones especiales para PIAR. | Protocolo de inclusión. | Función `fn_citacion_piar_tipo2` con condición `tiene_piar = true` |
| Se generarán alertas para PIAR con múltiples Tipo 2. | Monitoreo de estudiantes vulnerables. | Función `fn_generar_citacion_automatica` con condición `tiene_piar AND cantidad_tipo2 >= 2` |

### 📝 Acuerdos Correctivos

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las novedades tendrán acuerdos correctivos asociados. | Formalización de compromisos. | `acuerdos_correctivos` con `novedad_id`, `estudiante_id` |
| Los acuerdos tendrán descripción detallada. | Claridad en expectativas. | `acuerdos_correctivos.descripcion` |
| Los acuerdos tendrán compromiso del estudiante. | Formalización de responsabilidad. | `acuerdos_correctivos.compromiso` |
| Los acuerdos tendrán estado de seguimiento. | Control de cumplimiento. | `acuerdos_correctivos.estado` (ACTIVO, CUMPLIDO, INCUMPLIDO) |
| Se validará un acuerdo por novedad. | Prevención de duplicados. | CONSTRAINT `unica_novedad_acuerdo` UNIQUE(novedad_id) |

### 🛡️ Descargos de Estudiantes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los estudiantes podrán presentar descargos. | Derecho a defensa. | `descargos_estudiante` con `novedad_id`, `estudiante_id` |
| Los descargos tendrán descripción detallada. | Versión del estudiante. | `descargos_estudiante.descripcion` |
| Los descargos tendrán fecha de presentación. | Registro temporal. | `descargos_estudiante.fecha` |

### 📊 Respuestas a Novedades

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Las novedades tendrán respuestas de usuarios. | Diálogo y seguimiento. | `respuestas_novedad` con `novedad_id`, `usuario_id` |
| Las respuestas tendrán rol del usuario. | Identificación de quien responde. | `respuestas_novedad.rol` (ENUM) |
| Las respuestas tendrán mensaje. | Contenido de la comunicación. | `respuestas_novedad.mensaje` |
| Las respuestas tendrán fecha. | Registro temporal. | `respuestas_novedad.fecha` |

### ⚙️ Configuración Disciplinaria

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Cada colegio definirá su configuración disciplinaria. | Autonomía institucional. | `configuracion_disciplinaria` con `colegio_id` |
| Se definirán días de prescripción de novedades. | Limpieza automática de historial. | `configuracion_disciplinaria.dias_prescripcion` (default: 30) |
| Se definirá máximo de Tipo 2 antes de escalamiento. | Umbral de tolerancia. | `configuracion_disciplinaria.max_tipo2` (default: 3) |

### 🚨 Sistema de Alertas

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirá sistema de alertas automáticas. | Monitoreo proactivo de situaciones. | `alertas` con `estudiante_id`, `tipo`, `descripcion` |
| Las alertas tendrán tipo clasificado. | Categorización de alertas. | `alertas.tipo` (ALERTA_PIAR_DISCIPLINA, ALERTA_PIAR_TIPO2_ACUMULADO, etc.) |
| Las alertas tendrán estado de atención. | Control de seguimiento. | `alertas.atendida` (boolean) |
| Se validará una alerta activa por tipo. | Prevención de duplicados. | UNIQUE INDEX `unica_alerta_activa` WHERE `atendida = false` |

### 👪 Justificaciones de Acudientes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los acudientes podrán justificar novedades. | Participación de familia en proceso. | `justificaciones_acudiente` con `novedad_id`, `acudiente_id` |
| Las justificaciones tendrán texto detallado. | Explicación de situación. | `justificaciones_acudiente.justificacion` |
| Se validará una justificación por novedad. | Prevención de duplicados. | CONSTRAINT `justificaciones_acudiente_novedad_id_key` UNIQUE(novedad_id) |

---

## 📝 Documento 5: Arquitectura de Exámenes

### Objetivo
Definir el sistema de exámenes con banco de preguntas, configuración flexible y resultados automatizados.

### 📚 Banco de Preguntas

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirá banco de preguntas reutilizable. | Eficiencia en creación de exámenes. | `preguntas` como tabla independiente |
| Las preguntas tendrán tipo clasificado. | Diferentes formatos de pregunta. | `preguntas.tipo` (default: 'icfes') |
| Las preguntas tendrán texto de enunciado. | Contenido de la pregunta. | `preguntas.texto` |
| Las preguntas tendrán opciones en JSON. | Flexibilidad de estructura. | `preguntas.opciones` (JSONB) |
| Las preguntas tendrán respuesta correcta. | Validación automática. | `preguntas.respuesta_correcta` |
| Las preguntas tendrán rúbrica de IA opcional. | Soporte para evaluación automatizada. | `preguntas.rubrica_ia` |
| Las preguntas tendrán puntos máximos. | Ponderación de pregunta. | `preguntas.puntos_maximos` |
| Las preguntas tendrán explicación. | Retroalimentación educativa. | `preguntas.explicacion` |
| Las preguntas tendrán tema clasificado. | Organización por temas. | `preguntas.tema` |
| Las preguntas tendrán nivel de dificultad. | Clasificación por complejidad. | `preguntas.dificultad` |
| Las preguntas se vincularán a materia. | Asociación curricular. | `preguntas.materia_id` con FK a `materias` |
| Las preguntas tendrán fecha de creación. | Auditoría temporal. | `preguntas.fecha_creacion` |

### 📋 Tipos de Examen

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Existirán tipos de examen configurables. | Flexibilidad para diferentes formatos. | `tipo_examen` como tabla independiente |
| Los tipos de examen tendrán nombre descriptivo. | Identificación clara. | `tipo_examen.nombre` |
| Los tipos de examen tendrán descripción. | Detalle de características. | `tipo_examen.descripcion` |
| Los tipos de examen podrán tener contexto. | Soporte para preguntas con contexto común. | `tipo_examen.tiene_contexto` |
| Los tipos de examen podrán usar JSON. | Configuración flexible. | `tipo_examen.tiene_json` |
| Los tipos de examen podrán requerir grupo. | Exámenes por grupo o individuales. | `tipo_examen.requiere_grupo` |
| Los tipos de examen tendrán tiempo por defecto. | Duración estándar. | `tipo_examen.tiempo_por_defecto` (default: 30 minutos) |
| Los tipos de examen tendrán configuración JSON. | Parametrización avanzada. | `tipo_examen.configuracion` (JSONB) |
| Los tipos de examen podrán ser individuales. | Flexibilidad de modalidad. | `tipo_examen.disponible_individual` |

### 📝 Gestión de Exámenes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los exámenes tendrán título descriptivo. | Identificación clara. | `examenes.titulo` |
| Los exámenes tendrán descripción opcional. | Instrucciones adicionales. | `examenes.descripcion` |
| Los exámenes tendrán tiempo límite. | Control de duración. | `examenes.tiempo_limite_minutos` (default: 60) |
| Los exámenes tendrán archivo JSON opcional. | Importación de preguntas. | `examenes.archivo_json` |
| Los exámenes tendrán contenido JSON. | Almacenamiento de preguntas. | `examenes.contenido_json` (JSONB) |
| Los exámenes se vincularán a tipo de examen. | Clasificación de formato. | `examenes.tipo_examen_id` con FK a `tipo_examen` |
| Los exámenes se vincularán a materia. | Asociación curricular. | `examenes.materia_id` con FK a `materias` |
| Los exámenes se vincularán a colegio. | Pertenencia institucional. | `examenes.colegio_id` con FK a `colegios` |
| Los exámenes tendrán fecha de aplicación. | Programación temporal. | `examenes.fecha` |
| Se indexará contenido JSON para búsqueda. | Optimización de consultas. | INDEX `idx_examenes_contenido_json` (GIN) |

### 📊 Contenido de Exámenes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Los exámenes tendrán contenido versionado. | Control de cambios. | `examen_contenido` con `examen_id`, `version` |
| El contenido se almacenará en JSON. | Flexibilidad de estructura. | `examen_contenido.contenido_json` (JSONB) |
| Se validará unicidad de versión por examen. | Prevención de duplicados. | CONSTRAINT `examen_contenido_examen_id_version_key` UNIQUE(examen_id, version) |

### 📈 Resultados de Exámenes

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Se registrarán resultados por estudiante y examen. | Seguimiento individualizado. | `resultados_examen` con `estudiante_id`, `examen_id` |
| Los resultados tendrán estadísticas completas. | Análisis de desempeño. | `resultados_examen.total_preguntas`, `resultados_examen.respuestas_correctas`, `resultados_examen.respuestas_incorrectas` |
| Los resultados tendrán porcentaje calculado. | Medición relativa. | `resultados_examen.porcentaje` |
| Los resultados tendrán nota numérica. | Calificación cuantitativa. | `resultados_examen.nota_numerica` |
| Los resultados tendrán nota literal. | Calificación cualitativa. | `resultados_examen.literal` |
| Los resultados tendrán nivel de desempeño. | Clasificación automática. | `resultados_examen.nivel` (Bajo, Básico, Alto, Superior) |
| Los resultados tendrán fecha de finalización. | Control de tiempo. | `resultados_examen.fecha_finalizacion` |
| Los resultados tendrán archivo de cuestionario. | Evidencia documental. | `resultados_examen.cuestionario_archivo` |
| Se validará unicidad de resultado por estudiante-examen. | Prevención de duplicados. | CONSTRAINT `resultado_unico_estudiante_examen` UNIQUE(estudiante_id, examen_id) |
| Se validará rango de porcentaje (0-100). | Integridad de datos. | CONSTRAINT `chk_porcentaje` CHECK (porcentaje >= 0 AND porcentaje <= 100) |

### 📋 Detalle de Respuestas

| 📌 Decisión | 📝 Justificación | 🗄️ Impacto |
|-------------|------------------|------------|
| Se registrará detalle de cada respuesta. | Análisis granular de desempeño. | `respuestas_examen_detalle` con `resultado_examen_id` |
| El detalle tendrá número de pregunta. | Identificación de pregunta. | `respuestas_examen_detalle.numero_pregunta` |
| El detalle tendrá texto de pregunta. | Registro de contenido. | `respuestas_examen_detalle.texto_pregunta` |
| El detalle tendrá respuesta seleccionada. | Respuesta del estudiante. | `respuestas_examen_detalle.respuesta_seleccionada` |
| El detalle tendrá respuesta correcta. | Validación automática. | `respuestas_examen_detalle.respuesta_correcta` |
| El detalle tendrá indicador de correctitud. | Cálculo automático. | `respuestas_examen_detalle.es_correcta` |
| El detalle tendrá tiempo de respuesta. | Análisis de velocidad. | `respuestas_examen_detalle.tiempo_respuesta_seg` |

---

## 🗄️ Documento 6: Modelo de Datos

### Objetivo
Documentar las relaciones entre entidades y principios de diseño del modelo de datos.

### 🔗 Relaciones Principales

#### Jerarquía Institucional
```
colegios
  ├── sedes (1:N)
  ├── usuarios (1:N)
  ├── docentes (1:N)
  ├── estudiantes (1:N)
  ├── acudientes (1:N)
  ├── coordinadores (1:N)
  ├── periodos_academicos (1:N)
  ├── materias (N:M via plan_estudios)
  ├── grupos (1:N)
  ├── areas_gestion (1:N)
  ├── escala_evaluacion (1:N)
  ├── configuracion_evaluacion (1:1)
  ├── modelo_evaluacion_estudiante (1:N)
  ├── configuracion_disciplinaria (1:1)
  ├── configuracion_escalamiento (1:N)
  └── suscripciones (1:1)
```

#### Estructura Académica
```
materias
  ├── competencias_materia (1:N)
  │   └── indicadores_logro (1:N)
  ├── nivel_materia (1:N)
  └── preguntas (1:N)

grupos
  ├── grupo_materias (1:N)
  │   └── clases (1:N via grupo_materia_id)
  ├── grupo_areas (1:N)
  ├── directores_grupo (1:N)
  └── estudiantes (1:N)

clases
  ├── clase_estudiantes (1:N)
  └── asistencias (1:N)
```

#### Sistema de Evaluación
```
areas_gestion
  └── competencias (1:N)
      └── contribuciones (1:N)
          └── criterios_evaluacion (1:N via acuerdos_evaluacion)
              └── evaluacion_criterio (1:N via evaluacion_final)
                  └── evidencias (1:N)

acuerdos_evaluacion
  ├── criterios_evaluacion (1:N)
  ├── evaluacion_final (1:1)
  └── seguimientos (1:N)
```

#### Sistema Disciplinario
```
estudiantes
  ├── novedades (1:N)
  │   ├── acuerdos_correctivos (1:1)
  │   ├── descargos_estudiante (1:N)
  │   ├── respuestas_novedad (1:N)
  │   ├── justificaciones_acudiente (1:N)
  │   └── citaciones_acudiente (1:N)
  ├── piar (1:N)
  │   └── ajustes_razonables (1:N)
  └── alertas (1:N)
```

#### Sistema de Exámenes
```
tipo_examen
  └── examenes (1:N)
      ├── examen_contenido (1:N)
      └── resultados_examen (1:N)
          └── respuestas_examen_detalle (1:N)

preguntas
  └── examenes (N:M via contenido_json)
```

### 📊 Principios de Diseño

| Principio | Descripción | Implementación |
|-----------|-------------|----------------|
| **Multi-tenencia** | Todas las entidades pertenecen a un colegio | `colegio_id` en todas las tablas relevantes |
| **Soft Delete** | No se eliminan datos físicamente | Campos `activo` en todas las entidades |
| **Auditoría** | Se registra quién y cuándo crea/modifica | Campos `fecha_creacion`, `fecha_actualizacion`, `registrada_por` |
| **Integridad Referencial** | Foreign keys con acciones definidas | CASCADE para eliminación en cascada, RESTRICT para protección |
| **Validación en BD** | Reglas de negocio en base de datos | CONSTRAINTS CHECK para validaciones |
| **Índices Optimizados** | Búsqueda eficiente | Índices en campos de búsqueda frecuente |
| **JSON para Flexibilidad** | Datos semiestructurados | JSONB para configuraciones, preguntas, opciones |
| **ENUM para Clasificación** | Valores discretos definidos | Tipos ENUM para roles, estados, categorías |
| **Secuencias para IDs** | Generación automática de IDs | Secuencias PostgreSQL para todas las PKs |
| **Triggers para Automatización** | Lógica de negocio en BD | Triggers para escalamiento, citaciones, bloqueos |

### 🔐 Constraints de Integridad

| Tipo | Descripción | Ejemplo |
|------|-------------|---------|
| **PRIMARY KEY** | Identificador único de fila | `CONSTRAINT colegios_pkey PRIMARY KEY (id)` |
| **FOREIGN KEY** | Referencia a otra tabla | `CONSTRAINT fk_usuario_colegio FOREIGN KEY (colegio_id) REFERENCES colegios(id)` |
| **UNIQUE** | Sin duplicados en columna | `CONSTRAINT usuarios_email_key UNIQUE (email)` |
| **CHECK** | Validación de valor | `CONSTRAINT chk_calificacion_valida CHECK (calificacion >= 0 AND calificacion <= 5)` |
| **NOT NULL** | Campo obligatorio | `nombre varchar(150) NOT NULL` |
| **DEFAULT** | Valor por defecto | `activo bool DEFAULT true` |
| **UNIQUE INDEX PARTIAL** | Unicidad condicional | `UNIQUE INDEX unico_piar_activo WHERE (activo = true)` |

### 📈 Índices de Rendimiento

| Tabla | Índice | Tipo | Propósito |
|-------|--------|------|-----------|
| `usuarios` | `idx_usuarios_colegio_id` | btree | Búsqueda por colegio |
| `usuarios` | `idx_usuarios_rol` | btree | Búsqueda por rol |
| `usuarios` | `idx_usuarios_nombre` | btree | Búsqueda por nombre |
| `estudiantes` | `idx_estudiantes_documento` | btree | Búsqueda por documento |
| `examenes` | `idx_examenes_contenido_json` | gin | Búsqueda en JSON |
| `escala_evaluacion` | `idx_escala_colegio` | btree | Búsqueda por colegio |
| `plan_estudios` | `idx_plan_estudios_colegio` | btree | Búsqueda por colegio |
| `plan_estudios` | `idx_plan_estudios_grado` | btree | Búsqueda por grado |
| `preguntas` | `idx_preguntas_materia` | btree | Búsqueda por materia |
| `notification_logs` | `idx_notification_logs_estado_tipo` | btree partial | Búsqueda de notificaciones pendientes |

---

## 📜 Documento 7: Decisiones de Arquitectura

### Objetivo
Documentar las decisiones estratégicas, funcionales y técnicas que definen la arquitectura de SistPROF.

### 🏗️ Principios Rectores de SistPROF

| Principio | Descripción |
|-----------|-------------|
| **Multiinstitución** | Un único sistema para múltiples colegios con aislamiento de datos. |
| **Multisede** | Cada colegio puede operar varias sedes con configuración independiente. |
| **Configuración antes que programación** | Las reglas institucionales deben parametrizarse, no codificarse. |
| **Autonomía institucional** | Cada colegio define sus procesos, escalas y modelos de evaluación. |
| **Trazabilidad** | La información histórica se conserva mediante soft delete. |
| **Escalabilidad** | La arquitectura debe permitir crecimiento futuro sin refactorización. |
| **Flexibilidad académica** | Adaptación a diferentes modelos educativos y normativas. |
| **Automatización** | Los cálculos y procesos repetitivos deben ser automáticos. |
| **Seguridad por diseño** | Autenticación centralizada, roles y protección contra accesos indebidos. |
| **Inclusión** | Soporte completo para estudiantes con necesidades especiales (PIAR). |

### 🎯 Decisiones Estratégicas Más Importantes

| Prioridad | Decisión | Justificación |
|-----------|----------|---------------|
| ⭐⭐⭐⭐⭐ | SistPROF será multiinstitución (SaaS) | Modelo de negocio escalable que permite atender múltiples colegios con un único sistema. |
| ⭐⭐⭐⭐⭐ | Cada colegio tendrá su propio SIEE configurable | Cumplimiento normativo y adaptación a diferentes modelos educativos. |
| ⭐⭐⭐⭐⭐ | La evaluación estará centrada en competencias | Alineación con estándares educativos modernos y seguimiento real del aprendizaje. |
| ⭐⭐⭐⭐⭐ | Escalas cualitativas, cuantitativas y mixtas coexistirán | Flexibilidad para diferentes instituciones y normativas. |
| ⭐⭐⭐⭐⭐ | El modelo de evaluación será parametrizable | Evita reglas rígidas codificadas y permite adaptación institucional. |
| ⭐⭐⭐⭐⭐ | Las notas definitivas serán calculadas automáticamente | Reducción de errores manuales y consistencia en cálculos. |
| ⭐⭐⭐⭐⭐ | Los boletines se adaptarán a la configuración institucional | Cumplimiento de formatos requeridos por cada institución. |
| ⭐⭐⭐⭐⭐ | La configuración prevalecerá sobre reglas codificadas | Flexibilidad y mantenibilidad del sistema. |
| ⭐⭐⭐⭐⭐ | Existirá escalamiento automático de faltas disciplinarias | Aplicación consistente de reglas institucionales. |
| ⭐⭐⭐⭐⭐ | Se implementará sistema PIAR completo | Cumplimiento de normativa de inclusión y soporte a estudiantes vulnerables. |
| ⭐⭐⭐⭐ | Las citaciones a acudientes serán automáticas | Respuesta inmediata a eventos críticos y reducción de carga operativa. |
| ⭐⭐⭐⭐ | Existirá sistema de notificaciones asíncrono | No bloquear la aplicación principal y mejorar experiencia de usuario. |
| ⭐⭐⭐⭐ | Los exámenes soportarán configuración JSON | Flexibilidad para diferentes formatos de preguntas y estructuras. |
| ⭐⭐⭐⭐ | Los resultados de exámenes se calcularán automáticamente | Reducción de carga operativa y consistencia en calificaciones. |
| ⭐⭐⭐ | Se implementará control de ingreso con QR | Seguridad y registro automático de movimientos de estudiantes. |
| ⭐⭐⭐ | Existirá sistema de alertas proactivas | Monitoreo de situaciones críticas y prevención de problemas. |
| ⭐⭐⭐ | Los acuerdos de evaluación tendrán workflow (Borrador/Cerrado) | Control de proceso y protección de evaluación finalizada. |
| ⭐⭐⭐ | Se implementará middleware de autenticación y superusuario | Seguridad transversal y control de operaciones críticas. |
| ⭐⭐ | Los usuarios tendrán aprobación administrativa | Control de acceso y prevención de registros no autorizados. |
| ⭐⭐ | Existirá sistema de tokens de activación con expiración | Seguridad en proceso de activación de cuentas. |
| ⭐⭐ | Se implementará bloqueo por intentos fallidos | Protección contra ataques de fuerza bruta. |
| ⭐ | Los exámenes soportarán importación desde JSON | Facilita migración y creación masiva de exámenes. |
| ⭐ | Existirá banco de preguntas reutilizable | Eficiencia en creación de exámenes y consistencia curricular. |
| ⭐ | Los resultados de exámenes tendrán detalle por pregunta | Análisis granular de desempeño y retroalimentación educativa. |

### 📊 Resumen de Capacidades del Sistema

| Capacidad | Descripción | Estado |
|-----------|-------------|--------|
| **Gestión Multi-Colegio** | Administración de múltiples instituciones con aislamiento completo | ✅ Implementado |
| **Multi-Sede** | Soporte para colegios con múltiples ubicaciones físicas | ✅ Implementado |
| **Gestión de Usuarios** | 6 roles institucionales con autenticación centralizada | ✅ Implementado |
| **Plan de Estudios** | Definición de malla curricular por colegio y grado | ✅ Implementado |
| **Gestión de Grupos** | Organización de estudiantes con director asignado | ✅ Implementado |
| **Horarios y Clases** | Asignación de clases con validación de conflictos | ✅ Implementado |
| **Evaluación por Competencias** | Sistema completo de competencias, contribuciones y criterios | ✅ Implementado |
| **Escalas Configurables** | Soporte para escalas numéricas, cualitativas y mixtas | ✅ Implementado |
| **Boletines Automáticos** | Generación automática de boletines con promedios ponderados | ✅ Implementado |
| **Sistema Disciplinario** | Gestión de novedades con escalamiento automático | ✅ Implementado |
| **Sistema PIAR** | Soporte completo para estudiantes con necesidades especiales | ✅ Implementado |
| **Citaciones Automáticas** | Generación automática de citaciones a acudientes | ✅ Implementado |
| **Banco de Preguntas** | Repositorio de preguntas tipo ICFES reutilizables | ✅ Implementado |
| **Exámenes en Línea** | Creación y aplicación de exámenes con resultados automáticos | ✅ Implementado |
| **Control de Asistencia** | Registro de asistencia con validación de unicidad | ✅ Implementado |
| **Control de Ingreso QR** | Registro de ingreso/salida con token QR | ✅ Implementado |
| **Notificaciones Email** | Sistema de notificaciones con logs y estados | ✅ Implementado |
| **Suscripciones** | Control de suscripciones con período de prueba | ✅ Implementado |
| **Informes MEN** | Generación de informes para Ministerio de Educación | ✅ Implementado |
| **Auditoría Completa** | Trazabilidad de todas las operaciones con soft delete | ✅ Implementado |

---

## 🎓 Conclusión

Con estos **siete documentos** tenemos una base documental completa y sólida que describe la arquitectura de SistPROF en todas sus dimensiones:

### 📚 Documentos Generados

1. **🏫 Arquitectura Administrativa** - Multi-tenencia, usuarios, seguridad, suscripciones, notificaciones
2. **🎓 Arquitectura Académica** - Materias, grupos, clases, períodos, jornadas, docentes, estudiantes, acudientes
3. **📊 Arquitectura de Evaluación** - Competencias, criterios, acuerdos, escalas, modelo de evaluación, boletines
4. **⚖️ Arquitectura Disciplinaria** - Novedades, escalamiento, citaciones, PIAR, acuerdos correctivos, alertas
5. **📝 Arquitectura de Exámenes** - Banco de preguntas, tipos de examen, exámenes, resultados, detalle de respuestas
6. **🗄️ Modelo de Datos** - Relaciones, principios de diseño, constraints, índices
7. **📜 Decisiones de Arquitectura** - Principios rectores, decisiones estratégicas priorizadas, resumen de capacidades

### 🎯 Aspectos Clave de SistPROF

Estos documentos no describen únicamente **cómo funciona** SistPROF, sino también **por qué** fue diseñado de esta manera, las **decisiones estratégicas** tomadas, y los **principios rectores** que guían su evolución futura.

SistPROF es una plataforma **SaaS multiinstitucional** diseñada para ser:
- **Flexible** - Configuración antes que programación
- **Escalable** - Arquitectura preparada para crecimiento
- **Segura** - Autenticación centralizada y roles granulares
- **Automatizada** - Cálculos y procesos repetitivos automáticos
- **Inclusiva** - Soporte completo para estudiantes con necesidades especiales
- **Trazable** - Auditoría completa con soft delete
- **Adaptable** - Cada institución define sus propios procesos

¿Necesitas que profundice en algún documento específico o que genere documentación adicional sobre algún componente en particular?