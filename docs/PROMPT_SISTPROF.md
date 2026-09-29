# Reglas y Convenciones de Desarrollo - SistPROF

## Arquitectura Técnica
- Stack: Python (Flask), Jinja2, HTML5/CSS3 (Bootstrap), PostgreSQL, DBeaver.
- Base de datos actual: PostgreSQL en local/servidor.

## Convenciones de la Base de Datos
- Las materias asignadas a un docente NO están en `docente_materia`. La relación real es a través de la tabla `grupo_materias`.
- Para consultar las materias de un docente específico, siempre usar `grupo_materias` unida a `materias`.
- NUNCA usar `DELETE` directo en tablas maestras (como `materias`). Usar `UPDATE materias SET estado = false` para desactivar registros y no romper llaves foráneas.

## Desarrollo e Interfaz
- Las consultas de materias en combos y desplegables deben filtrar únicamente las asignaciones reales del docente activo (`GrupoMateria.docente_id == current_user.id`).
- Manejar con cuidado los tipos de datos en plantillas Jinja2 (acceso a diccionarios `p.get('campo')` vs. atributos de objeto `p.campo`).