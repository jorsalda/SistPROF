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
- usuarios.is_superadmin  <-- CRÍTICO, la app la usa

### Regla
Ninguna columna se elimina hasta que el usuario lo apruebe explícitamente.


---
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
Es redundancia tecnica, no rompe nada, pero limpia el schema.

### Plan de tratamiento
1. Confirmar que ambas FKs son realmente redundantes (misma definicion).
2. Eliminar una de las dos (probablemente `fk_examenes_tipo_examen`).
## TEMA-005: Tabla `historial_notas` no existe

**Prioridad:** Alta
**Estado:** Pendiente de tratamiento
**Fecha de registro:** 2026-10-08

### Contexto
Las funciones trigger `fn_auditar_evaluacion()` y `fn_auditar_componente()`
intentan escribir en una tabla `historial_notas` que NO existe en la BD.
Cualquier DELETE o UPDATE sobre `evaluaciones_estudiante` o
`notas_componente_estudiante` puede fallar con:
`UndefinedTable: no existe la relación «historial_notas»`.

Descubierto durante la migracion de `periodos_academicos` (un DELETE
en cascada disparo el trigger).

### Plan de tratamiento
1. Verificar el DDL esperado de `historial_notas` (columnas referenciadas por los triggers).
2. Crear la tabla con una migracion dedicada.
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
3. **Transversalización en tiempo real** entre la profesora PIAR y los docentes
   regulares (información compartida al instante).

### Estado actual del DDL (aproximado)
Tabla `piar`:
- Columnas actuales: id, estudiante_id, diagnostico, objetivos,
  fecha_inicio, fecha_fin, activo.
- NO tiene columna para profesional encargado.
- NO tiene mecanismo de seguimiento en tiempo real.

Tabla `ajustes_razonables`:
- Columnas actuales: id, piar_id, descripcion, aplicado,
  fecha_aplicacion, fecha_creacion.
- Relacionada con `piar` por piar_id.

Enum `rol_usuario`:
- Valores actuales: superadmin, admin_colegio, docente, estudiante,
  acudiente, coordinador, secretaria, portero.
- NO tiene rol especifico de "profesional PIAR".

### Analisis pendiente
1. Definir exactamente que debe mostrar el dashboard.
2. Definir como se modela el "profesional encargado":
   - Nueva columna en `piar`? (ej. `profesional_id` FK a usuarios)
   - Nuevo rol en `rol_usuario`? (ej. `profesional_piar`)
   - O reutilizar un rol existente?
3. Definir como modelar la transversalizacion:
   - Nueva tabla de seguimiento PIAR?
   - Reutilizar `seguimientos` o `novedades`?
   - Otro mecanismo?
4. Identificar queries y accesos por rol.

### Reglas
- NO tocar el DDL hasta que se haga el diseño completo.
- NO agregar columnas ni tablas sin analisis previo.
- NO agregar valores al enum `rol_usuario` sin aprobacion explicita.