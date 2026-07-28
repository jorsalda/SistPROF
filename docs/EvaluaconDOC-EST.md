
## 📚 Los DOS Sistemas de Evaluación

### 🧑‍🏫 Sistema 1: Evaluación del DOCENTE (Decreto 1278)
**¿Qué evalúa?** El desempeño profesional del docente según el Ministerio de Educación.

```
AreaGestion (áreas de gestión: pedagógica, administrativa, etc.)
    ↓
CompetenciaDocente (competencias del docente) → tabla "competencias"
    ↓
Contribucion (contribuciones a cada competencia)
    ↓
CriterioEvaluacion (criterios del acuerdo)
    ↓
AcuerdoEvaluacion (acuerdo anual del docente)
    ↓
EvaluacionFinal → EvaluacionCriterio (calificación del docente)
```

**¿Quién evalúa?** El coordinador/rector evalúa al docente.

---

### 🎓 Sistema 2: Evaluación del ESTUDIANTE (Académica)
**¿Qué evalúa?** El aprendizaje de los estudiantes en cada materia.

```
Materia
    ↓
CompetenciaEstudiante (competencias de la materia) → tabla "competencias_materia"
    ↓
IndicadorLogro (indicadores de logro)
    ↓
EvaluacionEstudiante (nota del estudiante por indicador y período)
```

**¿Quién evalúa?** El docente evalúa al estudiante.

---

## ✅ Lo que YA está en el sistema

| Sistema | Modelos | Rutas | Estado |
|---------|---------|-------|--------|
| **Evaluación Docente** (1278) | ✅ `CompetenciaDocente`, `AcuerdoEvaluacion`, `CriterioEvaluacion`, `EvaluacionCriterio`, `EvaluacionFinal` | ❌ NO hay rutas | Solo modelos |
| **Evaluación Estudiante** (Académica) | ✅ `CompetenciaEstudiante`, `IndicadorLogro`, `EvaluacionEstudiante` | ❌ NO hay rutas para ingresar notas | Solo modelos |

---

## 🚨 Lo que FALTA para el módulo docente

### Para el Sistema de Evaluación del ESTUDIANTE (lo que el docente usa día a día):

| # | Funcionalidad | Ruta propuesta | Estado |
|---|---------------|----------------|--------|
| 1 | Ver mis grupos/materias asignados | `/docentes/mis-grupos` | ❌ Falta |
| 2 | Ver indicadores de logro por materia | `/docentes/indicadores/<materia_id>` | ❌ Falta |
| 3 | **Ingresar notas por estudiante** | `/docentes/notas/<grupo_id>/<materia_id>/<periodo_id>` | ❌ **CRÍTICO** |
| 4 | Guardar notas en `evaluaciones_estudiante` | `/docentes/notas/guardar` | ❌ **CRÍTICO** |
| 5 | Ver boletines de mis estudiantes | `/docentes/boletines` | ❌ Falta |

### Para el Sistema de Evaluación del DOCENTE (Decreto 1278):

| # | Funcionalidad | Ruta propuesta | Estado |
|---|---------------|----------------|--------|
| 1 | Ver mi acuerdo de evaluación anual | `/docentes/mi-acuerdo` | ❌ Falta |
| 2 | Crear/editar acuerdo de evaluación | `/docentes/mi-acuerdo/editar` | ❌ Falta |
| 3 | Ver criterios de evaluación | `/docentes/mi-acuerdo/criterios` | ❌ Falta |
| 4 | Ver mi evaluación final (por coord/rector) | `/docentes/mi-evaluacion-final` | ❌ Falta |

---

## 🤔 Pregunta clave: ¿Por cuál empezamos?

| Opción | Descripción | Ventaja |
|--------|-------------|---------|
| **A** | Módulo de **ingreso de notas del estudiante** (Sistema 2) | Es lo que el docente usa **todos los días** en clase |
| **B** | Módulo de **acuerdo de evaluación docente** (Sistema 1 - Decreto 1278) | Es un requisito administrativo anual |
| **C** | Avanzar en paralelo, primero lo más urgente de cada uno | Balance |

---

## 🎯 Mi recomendación

Empezar por la **Opción A: Ingreso de notas del estudiante**, porque:
1. Es lo que el docente necesita **ya mismo** para el día a día
2. Los modelos (`EvaluacionEstudiante`, `IndicadorLogro`, `CompetenciaEstudiante`) ya están completos
3. Es la base para boletines y reportes
4. Sin esto, el sistema no sirve para su propósito principal

**¿Arrancamos con el módulo de ingreso de notas?**

Si me confirmas, te genero paso a paso:
1. ✅ Ruta `/docentes/mis-grupos` → listar grupos y materias del docente
2. ✅ Ruta `/docentes/notas/<grupo_id>/<materia_id>/<periodo_id>` → tabla para ingresar notas
3. ✅ Ruta `/docentes/notas/guardar` → guardar en `evaluaciones_estudiante`
4. ✅ Templates con interfaz clara

**¿Vamos con la Opción A?** 🚀