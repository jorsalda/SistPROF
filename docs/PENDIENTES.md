# PENDIENTES — SistPROF

Registro de temas pendientes que NO son parte del trabajo en curso.
Cada tema se retoma con la profundidad que requiere, en una sesión dedicada.

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

## TEMA-005: Tabla `historial_notas` no existe

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento
**Fecha de registro:** 2026-10-08

### Contexto
Las funciones trigger `fn_auditar_evaluacion()` y `fn_auditar_componente()` intentan escribir en una tabla `historial_notas` que NO existe en la BD. Cualquier DELETE o UPDATE sobre `evaluaciones_estudiante` o `notas_componente_estudiante` puede fallar con:
`UndefinedTable: no existe la relación «historial_notas»`.

Descubierto durante la migración de `periodos_academicos` (un DELETE en cascada disparó el trigger).

### Plan de tratamiento
1. Verificar el DDL esperado de `historial_notas` (columnas referenciadas por los triggers).
2. Crear la tabla con una migración dedicada.
3. Probar que los triggers funcionen sin error.
4. Alternativa temporal: deshabilitar los triggers hasta que se cree la tabla.

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
Extender el sistema de asistencia/QR que se esta desarrollando para
acudientes (asistencia a citaciones) y estudiantes (QR de portero) para
aplicarlo tambien a DOCENTES:
- Registro de llegada tarde de docentes.
- Asistencia a reuniones de docentes.
- Configurable por el admin del colegio.

### Contexto
Surgio como idea durante la sesion de desarrollo del modulo de citaciones
a acudientes. Se anota para retomarlo en el futuro, cuando los modulos
relacionados ya esten funcionando.

### Alcance tentativo
1. Definir como se registra la llegada tarde de docentes (QR, manual, otro).
2. Definir si aplica para reuniones internas del colegio.
3. Configuracion por el admin (horarios, tolerancias, tipos de reuniones).
4. Reportes de asistencia para el admin.

### Reglas
- NO implementar sin diseno previo aprobado.
- NO tocar la logica actual de asistencia de estudiantes sin autorizacion.