Aquí tienes el resumen dividido exactamente como lo pediste, siguiendo el formato de tabla técnica de tu ejemplo, pero con todo lo trabajado y solucionado en **este chat**.

---

# DOCUMENTO 1: `docs/RESUMEN_COMANDOS_EJECUTADOS.md`
*Este documento contiene los comandos exactos, scripts y queries SQL que se ejecutaron para modificar el sistema.*

```markdown
# 📋 RESUMEN EJECUTIVO: COMANDOS Y ACCIONES TÉCNICAS (Chat Docente-Estud)

| **COMANDO / ACCIÓN** | **PROPÓSITO TÉCNICO EN EL SISTEMA** |
| :--- | :--- |
| ## **MANTENIMIENTO DE BASE DE DATOS Y PERIODOS** | |
| `CREATE TABLE materias_backup_20261019 AS SELECT * FROM materias;` | **Backup preventivo.** Copia de seguridad de las 76 materias antes de la limpieza para evitar pérdida de datos. |
| `DELETE FROM materias WHERE id IN (1, 29, 42, 70, 76);` | **Limpieza de datos.** Elimina las 5 materias duplicadas de "Matemáticas" que confundían el dropdown de creación de exámenes. |
| `INSERT INTO materias (nombre, estado) VALUES ...;` | **Estandarización.** Inserta las 13 materias oficiales de un colegio colombiano (Biología, Física, Química, etc.). |
| `DELETE FROM periodos_academicos WHERE colegio_id = 45;` | **Reorganización.** Borra los 5 periodos viejos que estaban solapados y con nombres erróneos ("Curto Periodo"). |
| `INSERT INTO periodos_academicos (colegio_id, nombre, ...) VALUES ...;` | **Creación limpia.** Crea 3 periodos continuos (Primer, Segundo, Tercer) donde el fin de uno es el inicio del otro. |
| `UPDATE configuracion_periodo SET estado = 'ABIERTO', permite_editar_notas = true ...;` | **Apertura de ventana.** Habilita el Tercer Periodo (id 6) para que docentes y estudiantes puedan guardar notas hasta el 12/12/2026. |
| ## **CORRECCIÓN DE LÓGICA (BACKEND)** | |
| `if ev.calificacion is not None` | **Fix del "0.0".** Reemplaza a `if ev.calificacion` (que trataba el 0 como falso/inexistente). Ahora las notas de 0.0 se muestran en "Mis Calificaciones" y en la planilla del docente. |
| `if isinstance(p.opciones, list): opciones_arr = p.opciones` | **Manejo de formatos.** Permite que `crear_desde_banco` lea opciones si vienen como array (de la BD) o como objeto JSON. Evita que el examen se cree sin opciones. |
| `prog = ProgramacionExamen.query.filter_by(...).first()` | **El Puente.** Busca la programación del examen para obtener la competencia asociada y guardar la nota del examen automáticamente en `evaluaciones_estudiante`. |
| `if fecha_apertura_dt > datetime.now(): flash("Advertencia...")` | **Validación de fecha.** Advierte al docente si programa un examen con fecha futura, evitando que se pregunte por qué el estudiante no lo ve. |
| ## **CORRECCIÓN DE LÓGICA (FRONTEND)** | |
| `JSON.parse(e.target.result).preguntas` | **Lectura del motor.** `ClsEstudiante.js` espera que el JSON del examen tenga la clave `preguntas` para iterar sobre las preguntas del examen. |
| `contextoHtml += '<p>' + pregunta.contexto.texto + '</p>'` | **Fix visual.** Maneja el contexto del examen como objeto (`{tipo, texto}`) y no como string plano, evitando el molesto `[object Object]` en la pantalla del estudiante. |
| ## **CORRECCIÓN DE DATOS (MIGRACIÓN)** | |
| `UPDATE examenes SET materia_id = 54 WHERE materia_id IN (...);` | **Reasignación.** Mueve todos los exámenes de las materias duplicadas a la materia oficial (id 54). |
| `UPDATE resultados_examen SET materia_id = 54 WHERE materia_id IN (...);` | **Mantenimiento de integridad.** Reasigna los resultados históricos para que no queden huérfanos al borrar las materias viejas. |
| `usuario.password_hash = generate_password_hash('123456')` | **Recuperación de acceso.** Script en Python para resetear la contraseña de un estudiante y desbloquear su cuenta. |
```

---

# DOCUMENTO 2: `docs/RESUMEN_EXPLICACIONES_Y_CONTEXTO.md`
*Este documento explica el "por qué" de las acciones, el contexto del sistema y las lecciones aprendidas.*

```markdown
# 📋 RESUMEN EJECUTIVO: CONTEXTO Y EXPLICACIONES TÉCNICAS (Chat Docente-Estud)

| **COMPONENTE / PROBLEMA** | **EXPLICACIÓN TÉCNICA Y PROPÓSITO EN EL FLUJO ESCOLAR** |
| :--- | :--- |
| ## **FLUJO DE EXÁMENES (EL PUENTE)** | |
| **Modelo de Datos**<br>`examenes.contenido_json` (JSONB) | Los exámenes se crean con un JSON que contiene preguntas, opciones y respuestas. Este JSON se genera desde el banco de preguntas y se guarda en formato de array (`[{...}, {...}]`). |
| **El Desfase**<br>Array vs Objeto `{preguntas: []}` | El motor del estudiante esperaba un objeto con la clave `preguntas`, pero el backend enviaba un array directo. Esto causaba que las preguntas no cargaran y apareciera vacío en el frontend. |
| **El Puente (Backend)**<br>`EvaluacionEstudiante` | Cuando el estudiante termina un examen, el sistema califica y luego busca la competencia asociada al examen. Inyecta la nota en `evaluaciones_estudiante` (la misma tabla que usa la planilla del docente). |
| **El Bug de los 0.0**<br>`float(0) = False` | En Python, el número 0 se evalúa como falso. El sistema usaba `if ev.calificacion` para decidir si mostrar la nota. Al sacar 0.0, lo ocultaba. La solución fue usar `if ev.calificacion is not None`. |
| **Validación de Fechas**<br>`datetime.now()` vs `fecha_apertura` | El docente programaba exámenes para el futuro sin darse cuenta. El sistema bloqueaba su visualización correctamente, pero no avisaba al docente. Se agregó un `flash` de advertencia. |
| ## **MANTENIMIENTO Y LIMPIEZA** | |
| **Caos de Materias**<br>5 "Matemáticas" en BD | El sistema tenía materias duplicadas con el mismo nombre, lo que causaba confusión al asignar exámenes. Se limpiaron y estandarizaron a 13 materias oficiales de Colombia. |
| **Caos de Periodos**<br>5 periodos solapados | Los periodos académicos se solapaban en fechas y todos estaban activos. Esto rompía los filtros. Se crearon 3 periodos limpios (Ene-May, May-Ago, Ago-Dic). |
| **Backups Manuales**<br>`CREATE TABLE ... AS SELECT` | Se aprendió que antes de hacer un `DELETE` o `UPDATE` masivo, es vital crear una tabla temporal de backup (ej. `materias_backup_20261019`). |
| ## **HERRAMIENTAS Y ARQUITECTURA** | |
| **Herramientas de Desarrollo**<br>PyCharm + DBeaver | Se usó PyCharm para modificar el código Python y DBeaver para verificar la base de datos en tiempo real (SELECTs de validación antes y después de los cambios). |
| **Rendimiento del ORM**<br>`db.session.flush()` | Se usa `flush()` en lugar de `commit()` para obtener IDs de registros recién creados (ej. el ID del examen) y poder crear dependencias (preguntas, competencias) en la misma transacción atómica. |
| **Separación de Roles**<br>Admin vs Docente vs Estudiante | **Admin:** Configura periodos, escala y tipos de evaluación.<br>**Docente:** Crea exámenes, asigna a grupos y califica.<br>**Estudiante:** Presenta exámenes y ve sus notas en "Mis Calificaciones". |
| ## **LECCIONES APRENDIDAS** | |
| **Diagnóstico antes de acción**<br>SELECT antes de UPDATE | Nunca modificar la BD sin haber consultado primero los datos. Se evitó (parcialmente) perder información al revisar el estado de las tablas. |
| **Respeto al código funcional**<br>No tocar `ClsEstudiante.js` | El motor del estudiante funcionaba perfectamente. Se perdió tiempo intentando arreglar el JS cuando el problema era la data en la BD (opciones vacías) o el envío del JSON. |
| **El impacto del 0**<br>Validación de nullidad | En bases de datos y Python, `0` y `None` no son lo mismo. Se corrigió la lógica para tratar `0.0` como una nota válida en todos los cálculos y visualizaciones. |
```