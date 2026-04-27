* **colegios**
* **usuarios**
* **tokens_activación**
* **docentes**
* **estudiantes**
* **acudientes**
* **estudiante_acudiente**

Con estructura profesional:

✔ propósito
✔ estructura
✔ reglas de negocio
✔ relaciones
✔ funciones asociadas
✔ triggers críticos

Ahora seguimos con el siguiente bloque lógico, que sería:

**Bloque académico:**

1. materias
2. clases
3. clase_estudiantes
4. asistencias
5. periodos
6. competencias
7. indicadores
8. evaluaciones_estudiante

Y después:

**Bloque disciplinario:**

* novedades
* alertas
* citaciones
* descargos
* acuerdos correctivos
* justificaciones

Y luego:

**Bloque inclusión (PIAR):**

* piar
* ajustes_razonables


Listo. Ya agregué al documento todo el **bloque académico**:

✅ materias
✅ clases
✅ clase_estudiantes
✅ asistencias
✅ competencias_materia
✅ indicadores_logro
✅ evaluaciones_estudiante
✅ periodos

Con eso ya queda documentado:

* estructura académica
* matrícula interna por clase
* asistencia
* evaluación por competencias
* indicadores de logro
* boletines

Siguiente bloque recomendado: **disciplinario**, que en tu diseño es bastante fuerte y tiene automatizaciones importantes:

1. novedades
2. respuestas_novedad
3. alertas
4. citaciones_acudiente
5. descargos_estudiante
6. acuerdos_correctivos
7. justificaciones_acudiente

Después hacemos:

* PIAR y ajustes razonables
* permisos docentes
* evaluación docente
* funciones y triggers detallados


# Documentación Técnica DDL — SistPROF

## Módulo Base

---

## 1. Tabla: colegios

### Propósito

Almacena la información principal de cada institución educativa dentro del modelo multi-colegio.

### Estructura

| Campo     | Tipo    | Nulo | Default  | Descripción                |
| --------- | ------- | ---- | -------- | -------------------------- |
| id        | serial  | No   | —        | Identificador único        |
| nombre    | varchar | No   | —        | Nombre oficial del colegio |
| codigo    | varchar | No   | generado | Código único institucional |
| direccion | varchar | Sí   | —        | Dirección física           |
| telefono  | varchar | Sí   | —        | Teléfono institucional     |
| email     | varchar | Sí   | —        | Correo institucional       |
| activo    | boolean | No   | true     | Estado lógico              |

### Reglas de negocio

* Cada colegio debe tener código único.
* El sistema soporta múltiples colegios independientes.
* El código puede generarse automáticamente.

### Relaciones

* 1:N con usuarios
* 1:N con docentes
* 1:N con estudiantes
* 1:N con materias
* 1:N con clases

### Funciones asociadas

* generar_codigo_colegio()

---

## 2. Tabla: usuarios

### Propósito

Centraliza autenticación y control de acceso al sistema.

### Estructura

| Campo          | Tipo      | Nulo | Default | Descripción         |
| -------------- | --------- | ---- | ------- | ------------------- |
| id             | serial    | No   | —       | Identificador único |
| nombre         | varchar   | No   | —       | Nombre completo     |
| email          | varchar   | No   | —       | Correo único        |
| password_hash  | varchar   | No   | —       | Contraseña cifrada  |
| rol            | enum      | No   | —       | Rol del usuario     |
| activo         | boolean   | No   | true    | Estado de acceso    |
| fecha_creacion | timestamp | No   | now()   | Fecha creación      |

### Roles del sistema

* ADMIN
* COLEGIO
* DOCENTE
* ESTUDIANTE
* ACUDIENTE

### Reglas de negocio

* El email debe ser único.
* La autenticación depende del rol.
* Los tokens de activación dependen de esta tabla.

### Relaciones

* 1:N con tokens_activacion
* 1:N con respuestas_novedad

---

## 3. Tabla: tokens_activacion

### Propósito

Gestiona activación y validación inicial de cuentas.

### Estructura

| Campo            | Tipo         |
| ---------------- | ------------ |
| id               | serial       |
| usuario_id       | int          |
| token            | varchar(120) |
| fecha_expiracion | timestamp    |
| usado            | boolean      |

### Reglas de negocio

* Token único.
* Puede expirar.
* Se invalida al usarse.

### Relaciones

* N:1 con usuarios

---

## 4. Tabla: docentes

### Propósito

Almacena personal docente del colegio.

### Reglas de negocio

* Vinculado a colegio.
* Puede tener clases, permisos y evaluación docente.

### Relaciones

* 1:N con clases
* 1:N con permisos
* 1:N con acuerdos_evaluacion

---

## 5. Tabla: estudiantes

### Propósito

Gestiona estudiantes matriculados.

### Reglas de negocio

* Vinculados a colegio.
* Pueden tener acudientes, novedades, PIAR y asistencia.

### Relaciones

* 1:N con novedades
* 1:N con asistencias
* 1:N con PIAR
* N:N con acudientes

---

## 6. Tabla: acudientes

### Propósito

Representa responsables legales o familiares.

### Relaciones

* N:N con estudiantes
* 1:N con citaciones
* 1:N con justificaciones

---

## 7. Tabla: estudiante_acudiente

### Propósito

Tabla pivote para relación estudiante-acudiente.

### Restricciones

* unique(estudiante_id, acudiente_id)

---

## 8. Tabla: materias

### Propósito

Administra las asignaturas académicas de cada institución.

### Reglas de negocio

* Cada materia pertenece a un colegio.
* Puede asociarse a múltiples clases.
* Sirve como base para competencias e indicadores.

### Relaciones

* 1:N con clases
* 1:N con competencias_materia

---

## 9. Tabla: clases

### Propósito

Define la asignación académica de un docente por grado, grupo, materia y horario.

### Estructura clave

* docente_id
* colegio_id
* grado
* grupo
* materia
* dia
* hora_inicio
* hora_fin
* materia_id

### Restricciones

* horario_unico (docente, día, hora_inicio, hora_fin)

### Reglas de negocio

* Un docente no puede tener traslape de horario.
* Cada clase puede tener múltiples estudiantes.

### Relaciones

* N:1 con docentes
* N:1 con materias
* N:N con estudiantes
* 1:N con asistencias

---

## 10. Tabla: clase_estudiantes

### Propósito

Matrícula académica de estudiantes dentro de clases.

### Restricciones

* unique(clase_id, estudiante_id)

### Relaciones

* N:1 con clases
* N:1 con estudiantes

---

## 11. Tabla: asistencias

### Propósito

Control diario de asistencia por estudiante y clase.

### Campos clave

* estudiante_id
* clase_id
* fecha
* estado
* observacion
* registrada_por

### Restricciones

* Una asistencia por estudiante, clase y fecha.

### Reglas de negocio

* Evita duplicados diarios.
* Permite observaciones disciplinarias o justificadas.

### Relaciones

* N:1 con estudiantes
* N:1 con clases

---

## 12. Tabla: competencias_materia

### Propósito

Define competencias evaluables por materia.

### Reglas de negocio

* Cada competencia tiene porcentaje.
* La suma ideal por materia debe ser 100%.

### Relaciones

* N:1 con materias
* 1:N con indicadores_logro

---

## 13. Tabla: indicadores_logro

### Propósito

Desglosa indicadores específicos para evaluar competencias.

### Reglas de negocio

* Cada indicador pertenece a una competencia.
* Se usa para evaluación directa al estudiante.

### Relaciones

* N:1 con competencias_materia
* 1:N con evaluaciones_estudiante

---

## 14. Tabla: evaluaciones_estudiante

### Propósito

Registra calificaciones individuales por indicador.

### Reglas de negocio

* Cada evaluación pertenece a estudiante, indicador y periodo.
* Permite consolidación para boletines.

### Relaciones

* N:1 con estudiantes
* N:1 con indicadores_logro
* N:1 con periodos

### Funciones asociadas

* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()

---

## 15. Tabla: periodos

### Propósito

Define periodos académicos del año escolar.

### Reglas de negocio

* Cada periodo pertenece a un colegio.
* Orden secuencial académico.

### Relaciones

* 1:N con evaluaciones_estudiante

---

## 16. Tabla: novedades

### Propósito

Registro disciplinario y de convivencia de estudiantes.

### Campos clave

* estudiante_id
* tipo_novedad
* informe
* fecha
* hora
* gravedad
* registrada_por

### Reglas de negocio

* Cada novedad pertenece a un estudiante.
* Puede generar citaciones automáticas.
* Puede escalar de Tipo 2 a Tipo 3.
* Puede generar alertas PIAR.

### Triggers asociados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2

### Relaciones

* N:1 con estudiantes
* 1:N con respuestas_novedad
* 1:1 con acuerdos_correctivos
* 1:1 con descargos_estudiante
* 1:1 con justificaciones_acudiente

---

## 17. Tabla: respuestas_novedad

### Propósito

Permite trazabilidad conversacional sobre novedades.

### Reglas de negocio

* Puede responder docente, acudiente o administrador.
* Guarda historial de interacción.

### Relaciones

* N:1 con novedades
* N:1 con usuarios

---

## 18. Tabla: alertas

### Propósito

Genera alertas automáticas sobre eventos críticos.

### Reglas de negocio

* Solo una alerta activa por tipo y estudiante.
* Se marca como atendida cuando se resuelve.

### Restricciones

* unique alerta activa

### Relaciones

* N:1 con estudiantes

---

## 19. Tabla: citaciones_acudiente

### Propósito

Gestiona reuniones formales con acudientes.

### Tipos de origen

* TIPO_3
* PIAR_TIPO2
* PIAR_TIPO3

### Reglas de negocio

* Se generan automáticamente según reglas disciplinarias.
* Evita duplicidad por origen.

### Restricciones

* unique por novedad
* unique por tipo_origen

### Relaciones

* N:1 con estudiantes
* N:1 con acudientes
* N:1 con novedades

---

## 20. Tabla: descargos_estudiante

### Propósito

Registro de versión o explicación del estudiante sobre una novedad.

### Reglas de negocio

* Cada descargo se asocia a una novedad.
* Hace parte del debido proceso.

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 21. Tabla: acuerdos_correctivos

### Propósito

Formaliza compromisos correctivos derivados de novedades.

### Reglas de negocio

* Solo un acuerdo por novedad.
* Permite seguimiento posterior.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 22. Tabla: justificaciones_acudiente

### Propósito

Permite al acudiente justificar novedades o ausencias.

### Reglas de negocio

* Una sola justificación por novedad.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con acudientes
* N:1 con novedades

---

## Observaciones técnicas

### Triggers críticos documentados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2
* trg_bloquear_criterios

### Funciones críticas documentadas

* fn_generar_citacion_automatica()
* fn_citacion_piar_tipo2()
* fn_escalamiento_tipo2_a_tipo3()
* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()
* fn_informe_men()
* fn_informe_detalle()
* get_informe_men()
* calcular_nivel_desempeno()
* generar_codigo_colegio()


# Documentación Técnica DDL — SistPROF

## Módulo Base

---

## 1. Tabla: colegios

### Propósito

Almacena la información principal de cada institución educativa dentro del modelo multi-colegio.

### Estructura

| Campo     | Tipo    | Nulo | Default  | Descripción                |
| --------- | ------- | ---- | -------- | -------------------------- |
| id        | serial  | No   | —        | Identificador único        |
| nombre    | varchar | No   | —        | Nombre oficial del colegio |
| codigo    | varchar | No   | generado | Código único institucional |
| direccion | varchar | Sí   | —        | Dirección física           |
| telefono  | varchar | Sí   | —        | Teléfono institucional     |
| email     | varchar | Sí   | —        | Correo institucional       |
| activo    | boolean | No   | true     | Estado lógico              |

### Reglas de negocio

* Cada colegio debe tener código único.
* El sistema soporta múltiples colegios independientes.
* El código puede generarse automáticamente.

### Relaciones

* 1:N con usuarios
* 1:N con docentes
* 1:N con estudiantes
* 1:N con materias
* 1:N con clases

### Funciones asociadas

* generar_codigo_colegio()

---

## 2. Tabla: usuarios

### Propósito

Centraliza autenticación y control de acceso al sistema.

### Estructura

| Campo          | Tipo      | Nulo | Default | Descripción         |
| -------------- | --------- | ---- | ------- | ------------------- |
| id             | serial    | No   | —       | Identificador único |
| nombre         | varchar   | No   | —       | Nombre completo     |
| email          | varchar   | No   | —       | Correo único        |
| password_hash  | varchar   | No   | —       | Contraseña cifrada  |
| rol            | enum      | No   | —       | Rol del usuario     |
| activo         | boolean   | No   | true    | Estado de acceso    |
| fecha_creacion | timestamp | No   | now()   | Fecha creación      |

### Roles del sistema

* ADMIN
* COLEGIO
* DOCENTE
* ESTUDIANTE
* ACUDIENTE

### Reglas de negocio

* El email debe ser único.
* La autenticación depende del rol.
* Los tokens de activación dependen de esta tabla.

### Relaciones

* 1:N con tokens_activacion
* 1:N con respuestas_novedad

---

## 3. Tabla: tokens_activacion

### Propósito

Gestiona activación y validación inicial de cuentas.

### Estructura

| Campo            | Tipo         |
| ---------------- | ------------ |
| id               | serial       |
| usuario_id       | int          |
| token            | varchar(120) |
| fecha_expiracion | timestamp    |
| usado            | boolean      |

### Reglas de negocio

* Token único.
* Puede expirar.
* Se invalida al usarse.

### Relaciones

* N:1 con usuarios

---

## 4. Tabla: docentes

### Propósito

Almacena personal docente del colegio.

### Reglas de negocio

* Vinculado a colegio.
* Puede tener clases, permisos y evaluación docente.

### Relaciones

* 1:N con clases
* 1:N con permisos
* 1:N con acuerdos_evaluacion

---

## 5. Tabla: estudiantes

### Propósito

Gestiona estudiantes matriculados.

### Reglas de negocio

* Vinculados a colegio.
* Pueden tener acudientes, novedades, PIAR y asistencia.

### Relaciones

* 1:N con novedades
* 1:N con asistencias
* 1:N con PIAR
* N:N con acudientes

---

## 6. Tabla: acudientes

### Propósito

Representa responsables legales o familiares.

### Relaciones

* N:N con estudiantes
* 1:N con citaciones
* 1:N con justificaciones

---

## 7. Tabla: estudiante_acudiente

### Propósito

Tabla pivote para relación estudiante-acudiente.

### Restricciones

* unique(estudiante_id, acudiente_id)

---

## 8. Tabla: materias

### Propósito

Administra las asignaturas académicas de cada institución.

### Reglas de negocio

* Cada materia pertenece a un colegio.
* Puede asociarse a múltiples clases.
* Sirve como base para competencias e indicadores.

### Relaciones

* 1:N con clases
* 1:N con competencias_materia

---

## 9. Tabla: clases

### Propósito

Define la asignación académica de un docente por grado, grupo, materia y horario.

### Estructura clave

* docente_id
* colegio_id
* grado
* grupo
* materia
* dia
* hora_inicio
* hora_fin
* materia_id

### Restricciones

* horario_unico (docente, día, hora_inicio, hora_fin)

### Reglas de negocio

* Un docente no puede tener traslape de horario.
* Cada clase puede tener múltiples estudiantes.

### Relaciones

* N:1 con docentes
* N:1 con materias
* N:N con estudiantes
* 1:N con asistencias

---

## 10. Tabla: clase_estudiantes

### Propósito

Matrícula académica de estudiantes dentro de clases.

### Restricciones

* unique(clase_id, estudiante_id)

### Relaciones

* N:1 con clases
* N:1 con estudiantes

---

## 11. Tabla: asistencias

### Propósito

Control diario de asistencia por estudiante y clase.

### Campos clave

* estudiante_id
* clase_id
* fecha
* estado
* observacion
* registrada_por

### Restricciones

* Una asistencia por estudiante, clase y fecha.

### Reglas de negocio

* Evita duplicados diarios.
* Permite observaciones disciplinarias o justificadas.

### Relaciones

* N:1 con estudiantes
* N:1 con clases

---

## 12. Tabla: competencias_materia

### Propósito

Define competencias evaluables por materia.

### Reglas de negocio

* Cada competencia tiene porcentaje.
* La suma ideal por materia debe ser 100%.

### Relaciones

* N:1 con materias
* 1:N con indicadores_logro

---

## 13. Tabla: indicadores_logro

### Propósito

Desglosa indicadores específicos para evaluar competencias.

### Reglas de negocio

* Cada indicador pertenece a una competencia.
* Se usa para evaluación directa al estudiante.

### Relaciones

* N:1 con competencias_materia
* 1:N con evaluaciones_estudiante

---

## 14. Tabla: evaluaciones_estudiante

### Propósito

Registra calificaciones individuales por indicador.

### Reglas de negocio

* Cada evaluación pertenece a estudiante, indicador y periodo.
* Permite consolidación para boletines.

### Relaciones

* N:1 con estudiantes
* N:1 con indicadores_logro
* N:1 con periodos

### Funciones asociadas

* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()

---

## 15. Tabla: periodos

### Propósito

Define periodos académicos del año escolar.

### Reglas de negocio

* Cada periodo pertenece a un colegio.
* Orden secuencial académico.

### Relaciones

* 1:N con evaluaciones_estudiante

---

## 16. Tabla: novedades

### Propósito

Registro disciplinario y de convivencia de estudiantes.

### Campos clave

* estudiante_id
* tipo_novedad
* informe
* fecha
* hora
* gravedad
* registrada_por

### Reglas de negocio

* Cada novedad pertenece a un estudiante.
* Puede generar citaciones automáticas.
* Puede escalar de Tipo 2 a Tipo 3.
* Puede generar alertas PIAR.

### Triggers asociados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2

### Relaciones

* N:1 con estudiantes
* 1:N con respuestas_novedad
* 1:1 con acuerdos_correctivos
* 1:1 con descargos_estudiante
* 1:1 con justificaciones_acudiente

---

## 17. Tabla: respuestas_novedad

### Propósito

Permite trazabilidad conversacional sobre novedades.

### Reglas de negocio

* Puede responder docente, acudiente o administrador.
* Guarda historial de interacción.

### Relaciones

* N:1 con novedades
* N:1 con usuarios

---

## 18. Tabla: alertas

### Propósito

Genera alertas automáticas sobre eventos críticos.

### Reglas de negocio

* Solo una alerta activa por tipo y estudiante.
* Se marca como atendida cuando se resuelve.

### Restricciones

* unique alerta activa

### Relaciones

* N:1 con estudiantes

---

## 19. Tabla: citaciones_acudiente

### Propósito

Gestiona reuniones formales con acudientes.

### Tipos de origen

* TIPO_3
* PIAR_TIPO2
* PIAR_TIPO3

### Reglas de negocio

* Se generan automáticamente según reglas disciplinarias.
* Evita duplicidad por origen.

### Restricciones

* unique por novedad
* unique por tipo_origen

### Relaciones

* N:1 con estudiantes
* N:1 con acudientes
* N:1 con novedades

---

## 20. Tabla: descargos_estudiante

### Propósito

Registro de versión o explicación del estudiante sobre una novedad.

### Reglas de negocio

* Cada descargo se asocia a una novedad.
* Hace parte del debido proceso.

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 21. Tabla: acuerdos_correctivos

### Propósito

Formaliza compromisos correctivos derivados de novedades.

### Reglas de negocio

* Solo un acuerdo por novedad.
* Permite seguimiento posterior.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 22. Tabla: justificaciones_acudiente

### Propósito

Permite al acudiente justificar novedades o ausencias.

### Reglas de negocio

* Una sola justificación por novedad.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con acudientes
* N:1 con novedades

---

## 23. Tabla: piar

### Propósito

Gestiona el Plan Individual de Ajustes Razonables (PIAR) para estudiantes con necesidades específicas de apoyo.

### Campos clave

* estudiante_id
* diagnostico
* objetivos
* fecha_inicio
* fecha_fin
* activo

### Reglas de negocio

* Solo puede existir un PIAR activo por estudiante.
* Permite activar estrategias de inclusión.
* Interactúa con el módulo disciplinario.

### Restricciones

* Índice único parcial por estudiante cuando activo = true.

### Relaciones

* N:1 con estudiantes
* 1:N con ajustes_razonables

---

## 24. Tabla: ajustes_razonables

### Propósito

Registra adaptaciones pedagógicas derivadas de un PIAR.

### Campos clave

* piar_id
* descripcion
* aplicado
* fecha_aplicacion

### Reglas de negocio

* Cada ajuste depende de un PIAR.
* Puede marcarse como aplicado para trazabilidad.

### Relaciones

* N:1 con piar

---

## 25. Tabla: permisos

### Propósito

Gestiona permisos académicos y administrativos de docentes.

### Campos clave

* docente_id
* fecha_inicio
* fecha_fin
* tipo
* observacion
* colegio_id
* activo

### Reglas de negocio

* La fecha fin no puede ser menor a la fecha inicio.
* No afecta autenticación ni acceso al sistema.
* Solo controla disponibilidad laboral.

### Restricciones

* CHECK fecha_fin >= fecha_inicio

### Relaciones

* N:1 con docentes
* N:1 con colegios

---

## 26. Tabla: acuerdos_evaluacion

### Propósito

Documento base de evaluación anual del docente.

### Campos clave

* docente_id
* colegio_id
* anio
* estado

### Estados posibles

* BORRADOR
* CERRADO

### Reglas de negocio

* Solo un acuerdo por docente por año.
* Base principal de evaluación docente.

### Restricciones

* unique(docente_id, anio)

### Relaciones

* N:1 con docentes
* N:1 con colegios
* 1:N con criterios_evaluacion
* 1:N con seguimientos
* 1:1 con evaluacion_final

---

## 27. Tabla: criterios_evaluacion

### Propósito

Criterios específicos que el docente debe evidenciar.

### Reglas de negocio

* No se pueden modificar si el acuerdo está cerrado.

### Trigger asociado

* trg_bloquear_criterios

### Relaciones

* N:1 con acuerdos_evaluacion
* N:1 con contribuciones
* 1:N con evidencias

---

## 28. Tabla: evidencias

### Propósito

Evidencias cargadas por el docente para demostrar cumplimiento.

### Campos clave

* criterio_id
* descripcion
* tipo
* url
* aprobado

### Reglas de negocio

* Pueden ser revisadas y aprobadas por administración.

### Relaciones

* N:1 con criterios_evaluacion

---

## 29. Tabla: seguimientos

### Propósito

Registro de observaciones y recomendaciones durante la evaluación docente.

### Relaciones

* N:1 con acuerdos_evaluacion

---

## 30. Tabla: evaluacion_final

### Propósito

Cierre formal del proceso de evaluación docente.

### Reglas de negocio

* Solo una evaluación final por acuerdo.

### Restricciones

* unique(acuerdo_id)

### Relaciones

* 1:1 con acuerdos_evaluacion
* 1:N con evaluacion_criterio

---

## 31. Tabla: evaluacion_criterio

### Propósito

Calificación individual por criterio evaluado.

### Restricciones

* calificación entre 0 y 5.
* evaluación única por criterio.

### Relaciones

* N:1 con evaluacion_final
* N:1 con criterios_evaluacion

### Funciones asociadas

* fn_informe_men()
* fn_informe_detalle()
* get_informe_men()

---

## Observaciones técnicas

### Triggers críticos documentados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2
* trg_bloquear_criterios

### Funciones críticas documentadas

* fn_generar_citacion_automatica()
* fn_citacion_piar_tipo2()
* fn_escalamiento_tipo2_a_tipo3()
* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()
* fn_informe_men()
* fn_informe_detalle()
* get_informe_men()
* calcular_nivel_desempeno()
* generar_codigo_colegio()


# Documentación Técnica DDL — SistPROF

## Módulo Base

---

## 1. Tabla: colegios

### Propósito

Almacena la información principal de cada institución educativa dentro del modelo multi-colegio.

### Estructura

| Campo     | Tipo    | Nulo | Default  | Descripción                |
| --------- | ------- | ---- | -------- | -------------------------- |
| id        | serial  | No   | —        | Identificador único        |
| nombre    | varchar | No   | —        | Nombre oficial del colegio |
| codigo    | varchar | No   | generado | Código único institucional |
| direccion | varchar | Sí   | —        | Dirección física           |
| telefono  | varchar | Sí   | —        | Teléfono institucional     |
| email     | varchar | Sí   | —        | Correo institucional       |
| activo    | boolean | No   | true     | Estado lógico              |

### Reglas de negocio

* Cada colegio debe tener código único.
* El sistema soporta múltiples colegios independientes.
* El código puede generarse automáticamente.

### Relaciones

* 1:N con usuarios
* 1:N con docentes
* 1:N con estudiantes
* 1:N con materias
* 1:N con clases

### Funciones asociadas

* generar_codigo_colegio()

---

## 2. Tabla: usuarios

### Propósito

Centraliza autenticación y control de acceso al sistema.

### Estructura

| Campo          | Tipo      | Nulo | Default | Descripción         |
| -------------- | --------- | ---- | ------- | ------------------- |
| id             | serial    | No   | —       | Identificador único |
| nombre         | varchar   | No   | —       | Nombre completo     |
| email          | varchar   | No   | —       | Correo único        |
| password_hash  | varchar   | No   | —       | Contraseña cifrada  |
| rol            | enum      | No   | —       | Rol del usuario     |
| activo         | boolean   | No   | true    | Estado de acceso    |
| fecha_creacion | timestamp | No   | now()   | Fecha creación      |

### Roles del sistema

* ADMIN
* COLEGIO
* DOCENTE
* ESTUDIANTE
* ACUDIENTE

### Reglas de negocio

* El email debe ser único.
* La autenticación depende del rol.
* Los tokens de activación dependen de esta tabla.

### Relaciones

* 1:N con tokens_activacion
* 1:N con respuestas_novedad

---

## 3. Tabla: tokens_activacion

### Propósito

Gestiona activación y validación inicial de cuentas.

### Estructura

| Campo            | Tipo         |
| ---------------- | ------------ |
| id               | serial       |
| usuario_id       | int          |
| token            | varchar(120) |
| fecha_expiracion | timestamp    |
| usado            | boolean      |

### Reglas de negocio

* Token único.
* Puede expirar.
* Se invalida al usarse.

### Relaciones

* N:1 con usuarios

---

## 4. Tabla: docentes

### Propósito

Almacena personal docente del colegio.

### Reglas de negocio

* Vinculado a colegio.
* Puede tener clases, permisos y evaluación docente.

### Relaciones

* 1:N con clases
* 1:N con permisos
* 1:N con acuerdos_evaluacion

---

## 5. Tabla: estudiantes

### Propósito

Gestiona estudiantes matriculados.

### Reglas de negocio

* Vinculados a colegio.
* Pueden tener acudientes, novedades, PIAR y asistencia.

### Relaciones

* 1:N con novedades
* 1:N con asistencias
* 1:N con PIAR
* N:N con acudientes

---

## 6. Tabla: acudientes

### Propósito

Representa responsables legales o familiares.

### Relaciones

* N:N con estudiantes
* 1:N con citaciones
* 1:N con justificaciones

---

## 7. Tabla: estudiante_acudiente

### Propósito

Tabla pivote para relación estudiante-acudiente.

### Restricciones

* unique(estudiante_id, acudiente_id)

---

## 8. Tabla: materias

### Propósito

Administra las asignaturas académicas de cada institución.

### Reglas de negocio

* Cada materia pertenece a un colegio.
* Puede asociarse a múltiples clases.
* Sirve como base para competencias e indicadores.

### Relaciones

* 1:N con clases
* 1:N con competencias_materia

---

## 9. Tabla: clases

### Propósito

Define la asignación académica de un docente por grado, grupo, materia y horario.

### Estructura clave

* docente_id
* colegio_id
* grado
* grupo
* materia
* dia
* hora_inicio
* hora_fin
* materia_id

### Restricciones

* horario_unico (docente, día, hora_inicio, hora_fin)

### Reglas de negocio

* Un docente no puede tener traslape de horario.
* Cada clase puede tener múltiples estudiantes.

### Relaciones

* N:1 con docentes
* N:1 con materias
* N:N con estudiantes
* 1:N con asistencias

---

## 10. Tabla: clase_estudiantes

### Propósito

Matrícula académica de estudiantes dentro de clases.

### Restricciones

* unique(clase_id, estudiante_id)

### Relaciones

* N:1 con clases
* N:1 con estudiantes

---

## 11. Tabla: asistencias

### Propósito

Control diario de asistencia por estudiante y clase.

### Campos clave

* estudiante_id
* clase_id
* fecha
* estado
* observacion
* registrada_por

### Restricciones

* Una asistencia por estudiante, clase y fecha.

### Reglas de negocio

* Evita duplicados diarios.
* Permite observaciones disciplinarias o justificadas.

### Relaciones

* N:1 con estudiantes
* N:1 con clases

---

## 12. Tabla: competencias_materia

### Propósito

Define competencias evaluables por materia.

### Reglas de negocio

* Cada competencia tiene porcentaje.
* La suma ideal por materia debe ser 100%.

### Relaciones

* N:1 con materias
* 1:N con indicadores_logro

---

## 13. Tabla: indicadores_logro

### Propósito

Desglosa indicadores específicos para evaluar competencias.

### Reglas de negocio

* Cada indicador pertenece a una competencia.
* Se usa para evaluación directa al estudiante.

### Relaciones

* N:1 con competencias_materia
* 1:N con evaluaciones_estudiante

---

## 14. Tabla: evaluaciones_estudiante

### Propósito

Registra calificaciones individuales por indicador.

### Reglas de negocio

* Cada evaluación pertenece a estudiante, indicador y periodo.
* Permite consolidación para boletines.

### Relaciones

* N:1 con estudiantes
* N:1 con indicadores_logro
* N:1 con periodos

### Funciones asociadas

* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()

---

## 15. Tabla: periodos

### Propósito

Define periodos académicos del año escolar.

### Reglas de negocio

* Cada periodo pertenece a un colegio.
* Orden secuencial académico.

### Relaciones

* 1:N con evaluaciones_estudiante

---

## 16. Tabla: novedades

### Propósito

Registro disciplinario y de convivencia de estudiantes.

### Campos clave

* estudiante_id
* tipo_novedad
* informe
* fecha
* hora
* gravedad
* registrada_por

### Reglas de negocio

* Cada novedad pertenece a un estudiante.
* Puede generar citaciones automáticas.
* Puede escalar de Tipo 2 a Tipo 3.
* Puede generar alertas PIAR.

### Triggers asociados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2

### Relaciones

* N:1 con estudiantes
* 1:N con respuestas_novedad
* 1:1 con acuerdos_correctivos
* 1:1 con descargos_estudiante
* 1:1 con justificaciones_acudiente

---

## 17. Tabla: respuestas_novedad

### Propósito

Permite trazabilidad conversacional sobre novedades.

### Reglas de negocio

* Puede responder docente, acudiente o administrador.
* Guarda historial de interacción.

### Relaciones

* N:1 con novedades
* N:1 con usuarios

---

## 18. Tabla: alertas

### Propósito

Genera alertas automáticas sobre eventos críticos.

### Reglas de negocio

* Solo una alerta activa por tipo y estudiante.
* Se marca como atendida cuando se resuelve.

### Restricciones

* unique alerta activa

### Relaciones

* N:1 con estudiantes

---

## 19. Tabla: citaciones_acudiente

### Propósito

Gestiona reuniones formales con acudientes.

### Tipos de origen

* TIPO_3
* PIAR_TIPO2
* PIAR_TIPO3

### Reglas de negocio

* Se generan automáticamente según reglas disciplinarias.
* Evita duplicidad por origen.

### Restricciones

* unique por novedad
* unique por tipo_origen

### Relaciones

* N:1 con estudiantes
* N:1 con acudientes
* N:1 con novedades

---

## 20. Tabla: descargos_estudiante

### Propósito

Registro de versión o explicación del estudiante sobre una novedad.

### Reglas de negocio

* Cada descargo se asocia a una novedad.
* Hace parte del debido proceso.

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 21. Tabla: acuerdos_correctivos

### Propósito

Formaliza compromisos correctivos derivados de novedades.

### Reglas de negocio

* Solo un acuerdo por novedad.
* Permite seguimiento posterior.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con estudiantes
* N:1 con novedades

---

## 22. Tabla: justificaciones_acudiente

### Propósito

Permite al acudiente justificar novedades o ausencias.

### Reglas de negocio

* Una sola justificación por novedad.

### Restricciones

* unique(novedad_id)

### Relaciones

* N:1 con acudientes
* N:1 con novedades

---

## 23. Tabla: piar

### Propósito

Gestiona el Plan Individual de Ajustes Razonables (PIAR) para estudiantes con necesidades específicas de apoyo.

### Campos clave

* estudiante_id
* diagnostico
* objetivos
* fecha_inicio
* fecha_fin
* activo

### Reglas de negocio

* Solo puede existir un PIAR activo por estudiante.
* Permite activar estrategias de inclusión.
* Interactúa con el módulo disciplinario.

### Restricciones

* Índice único parcial por estudiante cuando activo = true.

### Relaciones

* N:1 con estudiantes
* 1:N con ajustes_razonables

---

## 24. Tabla: ajustes_razonables

### Propósito

Registra adaptaciones pedagógicas derivadas de un PIAR.

### Campos clave

* piar_id
* descripcion
* aplicado
* fecha_aplicacion

### Reglas de negocio

* Cada ajuste depende de un PIAR.
* Puede marcarse como aplicado para trazabilidad.

### Relaciones

* N:1 con piar

---

## 25. Tabla: permisos

### Propósito

Gestiona permisos académicos y administrativos de docentes.

### Campos clave

* docente_id
* fecha_inicio
* fecha_fin
* tipo
* observacion
* colegio_id
* activo

### Reglas de negocio

* La fecha fin no puede ser menor a la fecha inicio.
* No afecta autenticación ni acceso al sistema.
* Solo controla disponibilidad laboral.

### Restricciones

* CHECK fecha_fin >= fecha_inicio

### Relaciones

* N:1 con docentes
* N:1 con colegios

---

## 26. Tabla: acuerdos_evaluacion

### Propósito

Documento base de evaluación anual del docente.

### Campos clave

* docente_id
* colegio_id
* anio
* estado

### Estados posibles

* BORRADOR
* CERRADO

### Reglas de negocio

* Solo un acuerdo por docente por año.
* Base principal de evaluación docente.

### Restricciones

* unique(docente_id, anio)

### Relaciones

* N:1 con docentes
* N:1 con colegios
* 1:N con criterios_evaluacion
* 1:N con seguimientos
* 1:1 con evaluacion_final

---

## 27. Tabla: criterios_evaluacion

### Propósito

Criterios específicos que el docente debe evidenciar.

### Reglas de negocio

* No se pueden modificar si el acuerdo está cerrado.

### Trigger asociado

* trg_bloquear_criterios

### Relaciones

* N:1 con acuerdos_evaluacion
* N:1 con contribuciones
* 1:N con evidencias

---

## 28. Tabla: evidencias

### Propósito

Evidencias cargadas por el docente para demostrar cumplimiento.

### Campos clave

* criterio_id
* descripcion
* tipo
* url
* aprobado

### Reglas de negocio

* Pueden ser revisadas y aprobadas por administración.

### Relaciones

* N:1 con criterios_evaluacion

---

## 29. Tabla: seguimientos

### Propósito

Registro de observaciones y recomendaciones durante la evaluación docente.

### Relaciones

* N:1 con acuerdos_evaluacion

---

## 30. Tabla: evaluacion_final

### Propósito

Cierre formal del proceso de evaluación docente.

### Reglas de negocio

* Solo una evaluación final por acuerdo.

### Restricciones

* unique(acuerdo_id)

### Relaciones

* 1:1 con acuerdos_evaluacion
* 1:N con evaluacion_criterio

---

## 31. Tabla: evaluacion_criterio

### Propósito

Calificación individual por criterio evaluado.

### Restricciones

* calificación entre 0 y 5.
* evaluación única por criterio.

### Relaciones

* N:1 con evaluacion_final
* N:1 con criterios_evaluacion

### Funciones asociadas

* fn_informe_men()
* fn_informe_detalle()
* get_informe_men()

---

## Funciones, Triggers y Automatizaciones

---

## Funciones PL/pgSQL documentadas

### 1. generar_codigo_colegio()

### Propósito

Genera códigos únicos para instituciones.

### Uso

Creación automática de colegios.

---

### 2. calcular_nivel_desempeno()

### Propósito

Determina nivel académico según nota numérica.

### Rangos

* Bajo (<3.0)
* Básico (<3.9)
* Alto (<4.6)
* Superior (>=4.6)

---

### 3. fn_boletin_estudiante(estudiante, periodo)

### Propósito

Genera boletín básico por promedio de materia.

### Resultado

* materia
* promedio
* nivel

---

### 4. fn_boletin_estudiante_pro(estudiante, periodo)

### Propósito

Genera boletín profesional ponderado por competencias.

### Resultado

* materia
* promedio_materia
* ponderado
* total
* nivel

---

### 5. fn_informe_men(evaluacion_final)

### Propósito

Genera informe consolidado MEN para evaluación docente.

---

### 6. fn_informe_detalle(evaluacion_final)

### Propósito

Genera informe detallado por áreas, competencias y contribuciones.

---

### 7. get_informe_men(evaluacion_final)

### Propósito

Versión extendida de informe MEN.

---

## Triggers documentados

### 1. trg_escalamiento_tipo2

### Evento

BEFORE INSERT ON novedades

### Función

fn_escalamiento_tipo2_a_tipo3()

### Propósito

Escala automáticamente acumulaciones Tipo 2 a Tipo 3.

---

### 2. trg_citacion_automatica

### Evento

AFTER INSERT ON novedades

### Función

fn_generar_citacion_automatica()

### Propósito

Genera citación automática por faltas graves.

---

### 3. trg_citacion_piar_tipo2

### Evento

AFTER INSERT ON novedades

### Función

fn_citacion_piar_tipo2()

### Propósito

Genera citación automática especial para estudiantes PIAR.

---

### 4. trg_bloquear_criterios

### Evento

INSERT / UPDATE / DELETE

### Función

bloquear_criterios_si_cerrado()

### Propósito

Bloquea modificación de criterios cuando el acuerdo está cerrado.

---

## Enums del sistema

### rol_usuario

Valores:

* ADMIN
* COLEGIO
* DOCENTE
* ESTUDIANTE
* ACUDIENTE

---

### tipo_novedad_enum

Valores definidos según manual de convivencia.

---

### tipo_gravedad

Valores:

* Tipo 1
* Tipo 2
* Tipo 3

---

### dia_semana

Valores:

* Lunes
* Martes
* Miércoles
* Jueves
* Viernes

---

## Índices especiales

### Índices únicos parciales

#### PIAR activo único

* unico_piar_activo

#### Alerta activa única

* unica_alerta_activa

#### Citación única por origen

* unique_citacion_por_novedad
* unique_citacion_por_tipo

---

## Flujo automático de disciplina

NOVEDAD REGISTRADA
↓
Validación gravedad
↓
Escalamiento Tipo 2 → Tipo 3
↓
Generación automática de citación
↓
Generación de alerta PIAR
↓
Descargo estudiante
↓
Justificación acudiente
↓
Acuerdo correctivo

---

## Flujo de evaluación docente

Acuerdo anual
↓
Criterios
↓
Evidencias
↓
Seguimientos
↓
Evaluación final
↓
Informe MEN

---

## Observaciones técnicas

### Triggers críticos documentados

* trg_citacion_automatica
* trg_citacion_piar_tipo2
* trg_escalamiento_tipo2
* trg_bloquear_criterios

### Funciones críticas documentadas

* fn_generar_citacion_automatica()
* fn_citacion_piar_tipo2()
* fn_escalamiento_tipo2_a_tipo3()
* fn_boletin_estudiante()
* fn_boletin_estudiante_pro()
* fn_informe_men()
* fn_informe_detalle()
* get_informe_men()
* calcular_nivel_desempeno()
* generar_codigo_colegio()
