
---

## ARCHIVO 2 — `docs/PENDIENTES_Docente-Estud.md`

```markdown
# PENDIENTES — Chat: Docente-Estud (SistPROF)

> **Chat:** Docente-Estud (SistPROF) + Gestión Académica + Gestión Académica
> **Chat anterior:** Migración 1 y Privilegios (SistPROF)
> **Última actualización:** 2026-10-21
> **Estado:** Activo
> **Próximo paso:** Fase B.1 — Mi Horario / Validar Carga Docente

---

## CONTEXTO

Este chat cubre:
- Módulo **Estudiante** (autoservicio + CRUD admin).
- Módulo **Docente** (dashboard, permisos, planilla, observador, etc.).
- Motor de **Exámenes** y **Talleres** (movido a TEMAs 013–015).
- **Notificaciones** relacionadas (ingreso QR ya cerrado en chat anterior).

**Fuente de verdad:** DDL (no crear tablas, columnas ni enums nuevos).
**Convenio:** diagnóstico antes de acción, entregables completos, paso a paso con confirmación, respeto al código base, explicaciones técnicas claras, preguntas ante duda.

**Nota:** los pendientes cross-chat se movieron a `PENDIENTES.md` como TEMAs 013–023. Este archivo cubre solo lo específico del módulo Estudiante/Docente.

---

## FASE A — Estabilizar "Mis Calificaciones" (núcleo del estudiante)

- [ ] A.1 Revisar si `mis_calificaciones` debe usar **promedio ponderado** en vez de promedio simple.
- [ ] A.2 Incorporar ponderación por `competencias_materia.porcentaje`.
- [ ] A.3 Incluir `notas_componente_estudiante` (autoevaluación + examen final) en la definitiva.
- [ ] A.4 Respetar la **escala del colegio** (`escala_evaluacion`) en vez de umbrales hardcodeados (4.5/3.0/2.0).
- [ ] A.5 Resolver el desajuste de mayúsculas/title-case en `nivel_desempeño` (ver TEMA-017).
- [ ] A.6 Decidir si `enunciado_nivel` se mantiene como está o se cambia por un campo formal.
- [ ] A.7 Validar cálculo con datos reales (no de prueba).
- [ ] A.8 Decidir si `mis_calificaciones` reutiliza `fn_calcular_definitiva` (SQL) o mantiene lógica Python.
- [ ] A.9 Decidir cómo se configura la escala cualitativa por colegio (ver DEC.10).

---

## FASE B — Sidebar del estudiante

- [x] **B.1 Mi Horario**
  - [x] Endpoint `GET /estudiantes/mi-horario`
  - [ ] Query: `Clase` JOIN `GrupoMateria` JOIN `Materia` JOIN `Docente` WHERE grupo del estudiante
  - [ ] Agrupar por día de la semana
  - [ ] Template `estudiantes/mi_horario.html`
  - [ ] Link en `estudiante_base.html`

- [x] **B.2 Mi Asistencia**
  - [ ] Endpoint `GET /estudiantes/mi-asistencia`
  - [ ] Consolidado: total, presentes, tardes, ausentes, %
  - [ ] Detalle: últimos 50 registros
  - [ ] Template `estudiantes/mi_asistencia.html`
  - [ ] Link en sidebar

- [x] **B.3 Mi Observador**
  - [ ] Endpoint `GET /estudiantes/mi-observador`
  - [ ] Query: `Novedad` WHERE estudiante_id ORDER BY fecha DESC
  - [ ] Incluir `respuestas_novedad` (a confirmar)
  - [ ] Template `estudiantes/mi_observador.html`
  - [ ] Link en sidebar

- [x] **B.4 Mis Citaciones**
  - [ ] Endpoint `GET /estudiantes/mis-citaciones`
  - [ ] Query: `CitacionAcudiente` WHERE estudiante_id
  - [ ] Template `estudiantes/mis_citaciones.html`
  - [ ] Link en sidebar
  - [ ] Decidir: ¿solo lectura o permite confirmar asistencia? (ver DEC.9)

- [x] **B.5 Mi PIAR**
  - [ ] Endpoint `GET /estudiantes/mi-piar`
  - [ ] Query: `PIAR` WHERE estudiante_id AND activo = True
  - [ ] Decidir: ¿mostrar todo o solo resumen? (ver DEC.8)
  - [ ] Template `estudiantes/mi_piar.html`
  - [ ] Link condicional en sidebar (solo si tiene PIAR)

- [x] **B.6 Actualizar `estudiante_base.html`**
  - [ ] Agregar los 5 ítems nuevos
  - [ ] Respetar estilos existentes (`coordinador.css`)

---

## FASE C — Dashboard del estudiante (consolidado)

- [ ] C.1 Promedio general del periodo actual (no solo de exámenes).
- [ ] C.2 Notas por materia (mini resumen).
- [ ] C.3 Próximos exámenes programados.
- [ ] C.4 Asistencia acumulada.
- [ ] C.5 Últimas novedades del observador.

---

## FASE D — Módulo Docente

- [ ] **D.1 Dashboard del docente (contadores hoy en 0)**
  - [ ] D.1.1 Consulta "Mis Estudiantes (Director)" → `directores_grupo`.
  - [ ] D.1.2 Consulta "Mis Áreas Académicas" → `docente_areas` / `grupo_areas`.
  - [ ] D.1.3 Consulta "Grupos Asignados" → `grupo_materias` / `clases`.
  - [ ] D.1.4 Consulta "Mi Carga Académica" → listar materias + grupos + horario.
  - [ ] D.1.5 Consulta "Estudiantes para Calificar" → del grupo donde imparte.

- [ ] **D.2 Planilla de calificaciones**
  - [ ] Reutilizar cálculo de Fase A (promedio ponderado).
  - [ ] Decidir qué variantes se conservan (`planilla.html`, `planillaB2.html`, `planillaPRO.html`, `selector_planilla.html`).

- [ ] **D.3 Observador del docente**
  - [ ] Conectar con `novedades` reales.
  - [ ] Crear/editar novedades.

- [ ] **D.4 Citaciones del docente**
  - [ ] Conectar con `citaciones_acudiente`.

- [ ] **D.5 Banco de preguntas**
  - [ ] Verificar estado actual.

- [ ] **D.6 Gestión de competencias**
  - [ ] Verificar estado actual.

- [ ] **D.7 Seguimiento académico**
  - [ ] Verificar estado actual.

- [ ] **D.8 Permisos del docente**
  - [ ] ✅ Ya funcional (no tocar).


## FASE E — Gestión Académica y Configuración (Reciente)

- [x] **E.1 Restaurar arquitectura relacional de materias**
  - [x] Eliminar columna `nivel_educativo` de tabla `materias`.
  - [x] Corregir modelo SQLAlchemy `Materia` (quitar atributo obsoleto).
  - [x] Reparar consulta en `plan_estudios()` para usar `NivelMateria`.

- [x] **E.2 Interfaz de configuración profesional**
  - [x] Ruta `/dashboard/configurar-materias-por-nivel` funcional.
  - [x] Asignación visual de materias a niveles vía checkboxes.
  - [x] Población inicial de dimensiones (Preescolar) y académicas.

- [x] **E.3 Navegación optimizada**
  - [x] Crear menú desplegable "Gestión Académica" en sidebar.
  - [x] Agrupar: Plan de Estudios, Materias, Carga Académica, Configurar Niveles.
  - [x] JavaScript toggle + CSS integrado al diseño oscuro.

- [ ] **E.4 Nombres específicos por nivel (Pendiente)**
  - [ ] Evaluar necesidad de alias/nombre específico en `nivel_materia`.
  - [ ] Implementar campo opcional `nombre_especifico` si se requiere.
  - [ ] Ajustar template `plan_estudios.html` para mostrar alias cuando exista.

- [ ] **E.5 Validación de carga docente (Vinculado a D.1)**
  - [ ] Verificar que horas asignadas en Plan de Estudios reflejen carga real.
  - [ ] Conectar con dashboard docente para mostrar "Horas Semanales".

---

## DECISIONES PENDIENTES (necesitan tu confirmación)

- [ ] **DEC.1** ¿El examen debe mostrar feedback inmediato o diferido?
- [ ] **DEC.2** ¿La explicación de cada pregunta es visible para el estudiante?
- [ ] **DEC.3** ¿La IA corrige talleres sola o siempre pasa por el docente?
- [ ] **DEC.4** ¿La nota del examen va directo a `evaluaciones_estudiante` o pasa por revisión?
- [ ] **DEC.5** ¿El taller es un `TipoExamen` o un concepto aparte?
- [ ] **DEC.6** ¿La escala del literal (`S/A/B/b/I`) es oficial o inventada?
- [ ] **DEC.7** ¿El estudiante puede repetir un examen/taller?
- [ ] **DEC.8** ¿`Mi PIAR` muestra todo o solo resumen?
- [ ] **DEC.9** ¿`Mis Citaciones` es solo lectura o permite confirmar asistencia?
- [ ] **DEC.10** ¿La escala cualitativa varía por colegio o es fija?

---

## NOTAS

- El **módulo Portero** ya está cerrado (chat anterior).
- El **login con rol `portero`** ya funciona.
- La **notificación por ingreso QR** funciona con regla dinámica de horario.
- El **desfase UTC-5** en `notification_logs.fecha_creacion` es esperado.
- **No tocar** el módulo de permisos del docente (ya funciona).

---

## PRÓXIMO PASO

**Prioridad 1:** Fase B.1 — Mi Horario (Estudiante).
**Prioridad 2:** Fase E.5 — Validar que la carga académica configurada se refleje correctamente en el módulo docente (D.1.4).
**Nota:** La gestión de nombres específicos por nivel (E.4) queda en espera de confirmación del usuario sobre si es realmente necesaria o si el nombre global es suficiente.