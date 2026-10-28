# PENDIENTES — SistPROF

Registro de temas pendientes que NO son parte del trabajo en curso.
Cada tema se retoma con la profundidad que requiere, en una sesión dedicada.

> **Nota:** cuando un TEMA se resuelve, NO se borra. Se mueve a la sección
> "TEMAS CERRADOS" con fecha y nota. Así no perdemos historia.

---

## ESTADO DE CHATS

| Chat | Estado | Próximo paso | Archivo |
|---|---|---|---|
| Migración 1 y Privilegios (SistPROF) | Cerrado | — | (histórico, sin archivo) |
| Docente-Estud (SistPROF) | Activo | Fase B.1 — Mi Horario | PENDIENTES_Docente-Estud.md |

---

# TEMAS ABIERTOS

---

## TEMA-001: Reconciliar Supabase (producción) con local

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento
**Fecha de registro:** 2026-10-07

### Contexto
Durante la puesta en marcha de producción (Supabase), se aplicaron ajustes manuales en varias tablas para que el sistema funcionara. Esos ajustes no quedaron registrados en migraciones Alembic.

### Consecuencia
- Supabase y local NO están sincronizados.
- Alembic no conoce los cambios aplicados en Supabase.
- Aplicar migraciones directamente en Supabase puede fallar (columnas que ya existen, columnas que ya no existen, tipos distintos).

### Plan de tratamiento (cuando se aborde)
1. Terminar de alinear la BD local con los modelos SQLAlchemy (Bloques A, B, C).
2. Hacer un diff de schemas: local vs Supabase (solo lectura, sin tocar prod).
3. Identificar exactamente qué se cambió manualmente en Supabase.
4. Diseñar un SQL de reconciliación que lleve Supabase al mismo estado que local.
5. Probar en un clon de Supabase (nunca directo en producción).
6. Aplicar con respaldo previo.

### Reglas mientras se aborda
- NO tocar Supabase sin plan aprobado.
- NO correr `alembic upgrade head` contra Supabase.
- NO hacer `alembic stamp` en Supabase sin análisis previo.


### Objetos creados en local pendientes de replicar a Supabase
- `historial_notas` (tabla + 3 índices) — creada 2026-10-16 (ver TEMA-005)
- `fn_calcular_definitiva` (reemplazada 2026-10-16, ver Fase A)
- `fn_validar_periodo_evaluacion` (reemplazada 2026-10-16, ver TEMA-019)


---

## TEMA-002: Bloque C — Drops de columnas obsoletas

**Prioridad:** Media
**Estado:** Pendiente (acumulando)
**Fecha de registro:** 2026-10-07

### Contexto
Alembic detectó columnas en la BD que ya no están declaradas en los modelos SQLAlchemy. NO se han eliminado (decisión explícita: nada se borra sin autorización).

### Columnas pendientes de decisión (una por una)
- acuerdos_correctivos.descripcion
- citaciones_acudiente.tipo_origen, fecha, observaciones
- clase_estudiantes.id
- clases.grupo_id, materia_id
- competencias_materia.activo
- contribuciones.competencia_id, orden, fecha_creacion, activo
- criterios_evaluacion.contribucion_id, fecha_creacion
- escala_evaluacion.tipo_escala
- evaluacion_final.estado, observaciones_finales
- evidencias.fecha_creacion, observacion_admin
- examenes.fecha
- justificaciones_acudiente.justificacion
- materias.estado
- permisos.activo
- preguntas.contexto
- respuestas_examen_detalle.indicador_logro_id
- respuestas_novedad.rol
- resultados_examen.total_preguntas
- seguimientos.recomendaciones
- suscripciones.precio_base, limite_sedes, en_prueba, activo
- usuarios.is_superadmin

### Regla
Ninguna columna se elimina hasta que el usuario lo apruebe explícitamente.

---

## TEMA-004: FK duplicada en tabla `examenes`

**Prioridad:** Baja
**Estado:** Pendiente de tratamiento
**Fecha de registro:** 2026-10-08

### Contexto
La tabla `examenes` tiene DOS foreign keys hacia `tipo_examen`:
- `examenes_tipo_examen_id_fkey`
- `fk_examenes_tipo_examen`

Ambas hacen lo mismo: `tipo_examen_id -> tipo_examen(id)`.
Es redundancia técnica, no rompe nada, pero limpia el schema.

### Plan de tratamiento
1. Confirmar que ambas FKs son realmente redundantes (misma definición).
2. Eliminar una de las dos (probablemente `fk_examenes_tipo_examen`).

---

## TEMA-006: Módulo PIAR — Dashboard, Profesional Encargado y Transversalización

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento (requiere sesión dedicada de diseño)
**Fecha de registro:** 2026-10-08

### Contexto
El usuario requiere que el módulo PIAR incluya:
1. Un **dashboard** para el PIAR con analítica/indicadores.
2. Un **profesional encargado** del PIAR (rol específico con acceso).
3. **Transversalización en tiempo real** entre la profesora PIAR y los docentes regulares (información compartida al instante).

### Estado actual del DDL (aproximado)
Tabla `piar`:
- Columnas actuales: id, estudiante_id, diagnostico, objetivos, fecha_inicio, fecha_fin, activo.
- NO tiene columna para profesional encargado.
- NO tiene mecanismo de seguimiento en tiempo real.

Tabla `ajustes_razonables`:
- Columnas actuales: id, piar_id, descripcion, aplicado, fecha_aplicacion, fecha_creacion.
- Relacionada con `piar` por piar_id.

Enum `rol_usuario`:
- Valores actuales: superadmin, admin_colegio, docente, estudiante, acudiente, coordinador, secretaria, portero.
- NO tiene rol específico de "profesional PIAR".

### Análisis pendiente
1. Definir exactamente qué debe mostrar el dashboard.
2. Definir cómo se modela el "profesional encargado":
   - Nueva columna en `piar`? (ej. `profesional_id` FK a usuarios)
   - Nuevo rol en `rol_usuario`? (ej. `profesional_piar`)
   - O reutilizar un rol existente?
3. Definir cómo modelar la transversalización:
   - Nueva tabla de seguimiento PIAR?
   - Reutilizar `seguimientos` o `novedades`?
   - Otro mecanismo?
4. Identificar queries y accesos por rol.

### Reglas
- NO tocar el DDL hasta que se haga el diseño completo.
- NO agregar columnas ni tablas sin análisis previo.
- NO agregar valores al enum `rol_usuario` sin aprobación explícita.

---

## TEMA-007: Módulo Malla de Evaluación — Código pendiente

**Prioridad:** Media
**Estado:** Pendiente de tratamiento (requiere sesión dedicada)
**Fecha de registro:** 2026-10-12

### Contexto
El módulo Malla de Evaluación tiene la BD completa pero NO tiene código
(modelos, rutas, templates).

### Estado de la BD (ya migrado)
Tablas creadas:
- `malla_plantilla` (formato general del admin).
- `malla_plantilla_columna` (columnas del formato).
- `malla_evaluacion` (malla de cada docente).
- `malla_evaluacion_detalle` (contenido por competencia).

### Diseño acordado
- Admin crea plantilla con estructura de columnas.
- Docente crea su malla basada en la plantilla.
- Competencias e indicadores se seleccionan de listas existentes + texto libre.
- Coordinadores y admin ven todas las mallas.
- Profesional PIAR no tiene acceso.

### Pendiente
1. Modelos Python (`MallaPlantilla`, `MallaPlantillaColumna`, `MallaEvaluacion`, `MallaEvaluacionDetalle`).
2. Registrar en `app/models/__init__.py`.
3. Rutas CRUD.
4. Templates.
5. Lógica de copia de plantilla al crear malla.
6. Vistas de supervisión (coordinadores/admin).
7. Permisos en `permisos_usuario`.

---

## TEMA-008: Templates del portal acudiente rotos

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento
**Fecha de registro:** 2026-10-12

### Contexto
El portal del acudiente tiene templates faltantes o mal referenciados.

### Problemas encontrados

**1. Ruta mal escrita en `app/routes/acudiente.py` línea 56:**
- Llama a `acudiente/mis_estudiantes.html` (sin "s").
- El archivo real es `acudientes/mis_estudiantes.html`.

**2. Templates faltantes en `app/templates/acudientes/`:**
- `calificaciones.html` (usado en línea 97)
- `asistencia.html` (usado en línea 104)
- `examenes.html` (usado en línea 111)
- `novedades.html` (usado en línea 118)
- `citaciones.html` (usado en línea 125)
- `perfil.html` (usado en línea 132)

### Consecuencia
Cualquier clic en el sidebar del portal del acudiente da
500 Internal Server Error (TemplateNotFound).
El acudiente solo puede ver el dashboard.

### Plan de tratamiento
1. Corregir la ruta en línea 56 de `acudiente.py`.
2. Crear los 6 templates faltantes.
3. Probar cada endpoint.

---

## TEMA-010: QR de estudiantes — mejoras pendientes

**Prioridad:** Media
**Estado:** Pendiente de desarrollo
**Fecha de registro:** 2026-10-12

### Contexto
Actualmente el QR de estudiantes solo existe como **token en texto**
(generado con `secrets.token_hex(8)`). Se guarda en la columna
`estudiantes.qr_token` y se usa para búsquedas por URL.

**Lo que SÍ existe hoy:**
- Generación del token: `estudiante.generar_qr_token()`.
- Endpoint `estudiante.regenerar_qr(id)`.
- Endpoint `estudiante.buscar_qr(token)`.
- Uso del token para registro de asistencia.

**Lo que NO existe hoy (confirmado por grep):**
- Generación de imágenes QR (códigos visuales para imprimir).
- Lector de QR por cámara (html5-qrcode o similar).
- QR específico para exámenes.

### Mejoras pendientes

**A) Generar imágenes de QR para imprimir.**
- Requiere librería tipo `qrcode` o `Pillow`.
- El docente o secretaría podría descargar el QR visual de cada estudiante.
- Útil para carnets, listas de asistencia, etc.

**B) Lector de QR desde la cámara.**
- Requiere `html5-qrcode` (JavaScript) en el frontend.
- Ya existe el lector USB en el módulo portero (`lector_qr.html`), pero
  falta la versión con cámara del navegador.
- Útil para tablets o celulares.

**C) QR para exámenes.**
- Identificar al estudiante que va a presentar un examen.
- Podría vincularse con el módulo de exámenes para validar identidad.
- Requiere diseño (¿qué se valida? ¿asistencia? ¿autenticación?).

### Plan de tratamiento
1. Definir cuál de las 3 mejoras tiene prioridad.
2. Diseñar cada mejora en sesión dedicada.
3. Implementar y probar.

### Reglas
- No tocar la lógica actual del QR sin autorización.
- Mantener compatibilidad con el módulo portero.

---

## TEMA-012: Asistencia y llegada tarde de docentes (a futuro)

**Prioridad:** Baja
**Estado:** Idea para futuro (no requiere acción inmediata)
**Fecha de registro:** 2026-10-12

### Idea
Extender el sistema de asistencia/QR que se está desarrollando para
acudientes (asistencia a citaciones) y estudiantes (QR de portero) para
aplicarlo también a DOCENTES:
- Registro de llegada tarde de docentes.
- Asistencia a reuniones de docentes.
- Configurable por el admin del colegio.

### Contexto
Surgió como idea durante la sesión de desarrollo del módulo de citaciones
a acudientes. Se anota para retomarlo en el futuro, cuando los módulos
relacionados ya estén funcionando.

### Alcance tentativo
1. Definir cómo se registra la llegada tarde de docentes (QR, manual, otro).
2. Definir si aplica para reuniones internas del colegio.
3. Configuración por el admin (horarios, tolerancias, tipos de reuniones).
4. Reportes de asistencia para el admin.

### Reglas
- NO implementar sin diseño previo aprobado.
- NO tocar la lógica actual de asistencia de estudiantes sin autorización.

---

## TEMA-013: Motor de Exámenes — Rediseño

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento (sesión dedicada)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
El motor de exámenes tiene problemas estructurales:
- Rutas duplicadas entre `api_examen_bp` y `examen_bp`.
- Formato JSON desajustado entre `contenido_json` (`{opciones:{A,B,C,D}}`) y `ClsEstudiante.js` (espera `[array]`).
- El estudiante puede cambiar cantidad de preguntas y tiempo (debe fijarlos el docente).
- No se respeta `puntos_maximos` (todo vale 1).
- No se respeta `tiempo_limite_minutos`.
- `materia_id = 1` hardcodeado en `api_examen_bp.guardar_resultado`.
- No valida `fecha_apertura` / `fecha_cierre` al enviar.

### Modelo conceptual (ya definido)
- **Examen** = respuesta única, sin argumentación de contexto, corrección automática.
- 3 vías de creación: IA (opcional), Manual, Parser ICFES.
- El docente fija cantidad, tiempo y competencia.
- Aleatoriedad en orden de preguntas y opciones.

### Pendiente
Rediseñar el motor respetando el DDL actual.

---

## TEMA-014: Motor de Talleres — Diseño desde cero

**Prioridad:** Alta
**Estado:** Pendiente de diseño (sesión dedicada)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
**Taller** = evaluación que requiere argumentación y desarrollo. Respuesta abierta, no única. Corrección por rúbrica (IA + docente).

### Modelo conceptual (ya definido)
- Requiere argumentación del contexto.
- Respuesta abierta (no única).
- Se evalúa proceso, no solo resultado.
- Corrección por rúbrica (`rubrica_ia`) + docente.
- 3 vías de creación: IA (opcional), Manual, Parser.

### Pendiente
- Definir si "taller" es un `TipoExamen` o concepto aparte.
- Preguntas abiertas con `rubrica_ia`.
- Implementar corrección por IA con rúbrica (hoy NO lo hace).
- Definir rol del docente en la corrección (¿obligatoria o solo cuando IA falla?).
- 3 vías de creación — análogo a exámenes.
- Definir tabla de resultados (¿reutilizar `resultados_examen`?).

---

## TEMA-015: Conectar exámenes/talleres al boletín oficial

**Prioridad:** Media
**Estado:** Pendiente
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
`ResultadoExamen.nota_numerica` no alimenta `evaluaciones_estudiante`. El examen queda aislado del boletín.

### Pendiente
- Decidir si la nota va directo a `evaluaciones_estudiante` o pasa por revisión.
- Vincular con `ProgramacionExamen.competencia_materia_id`.
- Que aparezca en "Mis Calificaciones" del estudiante y en la planilla del docente.

---

## TEMA-016: Unificar módulo de permisos (4 rutas duplicadas)

**Prioridad:** Media
**Estado:** Pendiente
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
Hay 4 rutas para el mismo concepto:
- `permiso_bp` (`/dashboard/permisos`) — canónico admin.
- `colegio_bp` (mismo prefijo `/dashboard` — huérfano por orden de registro).
- `docente_bp` (`/docentes/mis-permisos`) — autoservicio.
- `coordinador_bp` (`/coordinador/permisos`) — solo lectura.

### Pendiente
- Decidir blueprint canónico.
- Eliminar duplicados (con autorización explícita).
- Eliminar templates huérfanos.

---

## TEMA-017: Doble enum `nivel_desempeño` (mayúsculas vs title-case)

**Prioridad:** Alta
**Estado:** Pendiente (bug silencioso)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
En el DDL hay DOS enums distintos:
- `nivel_desempeno` → `'SUPERIOR','ALTO','BASICO','BAJO'`
- `niveldesempeno` → `'BAJO','BASICO','ALTO','SUPERIOR'`

Pero el modelo Python `IndicadorLogro` declara:
```python
NivelDesempenoEnum = ENUM('Bajo', 'Basico', 'Alto', 'Superior', ...)

**Consecuencia:** el tooltip `enunciado_nivel` en "Mis Calificaciones" nunca matchea porque compara `'BAJO'` (BD) vs `'Bajo'` (Python).

---

## TEMA-018: `materia_id = 1` hardcodeado

**Prioridad:** Alta
**Estado:** Pendiente (bug)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
`api_examen_bp.guardar_resultado` guarda `materia_id=1` sin importar el examen.

### Pendiente
Tomar `materia_id` del examen real.

---

## TEMA-020: Trigger `fn_generar_citacion_automatica` usa columna inexistente

**Prioridad:** Media
**Estado:** Pendiente
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
Usa `alertas.atendida` que no existe. La columna real es `alertas.activa`.

### Pendiente
Corregir el trigger.

---

## TEMA-021: `configuracion_escalamiento` vs `fn_escalamiento_tipo2_a_tipo3`

**Prioridad:** Media
**Estado:** Pendiente
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
La tabla tiene `tipo_origen`, `cantidad`, `tipo_destino`.
La función lee `usar_tiempo`, `dias_evaluacion`, `cantidad_tipo2`, `institucion_id`.
→ Incompatibilidad.

### Pendiente
Alinear tabla y función.

---

## TEMA-022: Notificaciones al acudiente/docente en flujo académico

**Prioridad:** Media
**Estado:** Pendiente (por definir)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
Hoy hay notificación por `ingreso_qr`. Pero no hay notificación cuando:
- Se crea una novedad (observador).
- Se genera una citación.
- Se publica una calificación.
- Se asigna un examen.

### Pendiente
Definir qué eventos notificar y a quién.

---

## TEMA-023: Mover CRUD de estudiantes a `secretaria_bp`

**Prioridad:** Baja
**Estado:** Pendiente (opcional, grande)
**Fecha de registro:** 2026-10-14
**Origen:** Chat Docente-Estud

### Contexto
`estudiante_bp` mezcla autoservicio del estudiante con CRUD administrativo de secretaría.

### Pendiente
Decidir si se separa (refactor grande) o se deja.

---

## TEMA-024: Validación de aislamiento multi-tenant en `grupo_materias`

**Prioridad:** Alta
**Estado:** Pendiente (requiere migración formal)
**Fecha de registro:** 2026-10-15
**Origen:** Chat Docente-Estud

### Contexto
Durante el diagnóstico del módulo de competencias se descubrió que `grupo_materias` permite insertar asignaciones cruzadas entre colegios sin que la BD lo impida.

**Ejemplo real (local):** se insertó un docente del colegio 45 en grupos del colegio 43. La BD lo aceptó.

### Problema
`grupo_materias` no tiene `colegio_id` ni constraint que valide `docente.colegio_id == grupo.colegio_id`.

### Consecuencia
- Un docente del colegio A podría ver/calificar estudiantes del colegio B.
- Violación del aislamiento multi-tenant.
- Cualquier INSERT (manual, script, bug) puede cruzar colegios.

### Plan de tratamiento (cuando se haga migración formal)
1. Agregar columna `colegio_id` a `grupo_materias`.
2. Backfill desde `grupos.colegio_id`.
3. Constraint compuesta `(grupo_id, colegio_id)` FK a `grupos(id, colegio_id)`.
4. Opcional: trigger que valide `docente.colegio_id == grupo.colegio_id`.
5. Validar datos existentes (buscar cruces).
6. Probar en clon de Supabase antes de aplicar en producción.

### Reglas
- NO agregar columnas sin análisis previo.
- Coordinar con TEMA-001.

---

## TEMA-025: Tabla `configuracion_evaluacion` referenciada pero inexistente

**Prioridad:** Media
**Estado:** Pendiente (requiere análisis formal)
**Fecha de registro:** 2026-10-16
**Origen:** Chat Docente-Estud

### Contexto
En `app/routes/docente_routes.py` (función `ver_planilla`, ~línea 955) hay una consulta:

```sql
SELECT tipo_captura FROM configuracion_evaluacion WHERE colegio_id = :cid
```

La tabla `configuracion_evaluacion` NO existe en el DDL ni en la BD local. Solo aparece en esa consulta (confirmado con `grep -rn "configuracion_evaluacion"`).

### Consecuencia
Al abrir la planilla del docente, el endpoint lanza `UndefinedTable` y devuelve 500.

### Mitigación temporal aplicada (2026-10-16)
Se agregó un `try/except` alrededor de la consulta en `ver_planilla`:
- Si la tabla existe → usa el valor de BD.
- Si no existe → usa `"NUMERICA"` por defecto (comportamiento previsto originalmente).

### Pendiente (análisis formal)
1. Definir si la tabla debe existir:
   - ¿Qué columnas tendría? (mínimo: `colegio_id`, `tipo_captura`)
   - ¿Qué valores válidos? (`NUMERICA`, `CUALITATIVA`, otros)
   - ¿Se relaciona con `escala_evaluacion`?
2. Si se decide crearla:
   - Migración Alembic dedicada.
   - Modelo Python.
   - Endpoint + template para que el admin la configure.
   - Replicar a Supabase (coordinar con TEMA-001).
3. Si se decide NO crearla:
   - Quitar la consulta del código (dejar `tipo_captura = "NUMERICA"` fijo).
   - Eliminar el `try/except` temporal.

### Reglas
- NO crear la tabla sin análisis previo.
- NO tocar el DDL hasta tener diseño aprobado.
- Coordinar con TEMA-001 (reconciliación Supabase vs local).


# TEMAS CERRADOS

<!--
Cuando un TEMA se resuelva, moverlo aquí con esta estructura:

## TEMA-XXX: Título
**Cerrado:** YYYY-MM-DD
**Nota:** Qué se hizo, cómo se resolvió.

NO borrar. La historia sirve.
-->

## TEMA-005: Tabla `historial_notas` no existe

**Cerrado:** 2026-10-16
**Nota:** Se creó la tabla `historial_notas` en local con 11 columnas + `id` (PK) + `fecha_cambio` + 3 índices (estudiante_id, tabla_origen+registro_id, fecha_cambio DESC). Los triggers `fn_auditar_evaluacion` y `fn_auditar_componente` ahora escriben correctamente. Verificado con guardado real desde la planilla del docente.

---

## TEMA-019: `fn_validar_periodo_evaluacion` usa tabla vieja `periodos`

**Cerrado:** 2026-10-16
**Nota:** Se reemplazó la función con `CREATE OR REPLACE`. Único cambio: `FROM periodos p` → `FROM periodos_academicos p`. Verificado con guardado real desde la planilla del docente.

---

_(pendiente de réplica a Supabase — coordinar con TEMA-001)_
