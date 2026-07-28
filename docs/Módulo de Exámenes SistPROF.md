# 📋 Hoja de Ruta del Módulo de Exámenes SistPROF"
| **LO QUE TENEMOS (✅ Completado)** | **LO QUE FALTA (🔲 Pendiente)** |
|-----------------------------------|--------------------------------|
| **1. CREACIÓN DE EXÁMENES CON IA** | **2. BANCO DE PREGUNTAS - 3 FORMAS DE ALIMENTARLO** |
| ✅ Docente sube PDF/DOCX |  **Opción A: IA Generativa** (ya existe) |
| ✅ IA (Gemini) genera preguntas tipo ICFES | - Docente sube PDF → IA genera preguntas → JSON |
| ✅ Revisión y edición en preview | - Ya funciona, pero necesita integración |
| ✅ Guardado en `examenes.contenido_json` | |
| ✅ Alimentación de tabla `preguntas` | 🔲 **Opción B: Subida de Cuestionario ICFES** (NUEVO) |
| ✅ Formateo automático a JSON | - Docente sube PDF con preguntas YA formuladas |
| | - Sistema detecta patrón: "Pregunta X", opciones A/B/C/D |
| | - Extrae: texto, opciones, respuesta correcta, explicación |
| | - Convierte a JSON automáticamente |
| | - Guarda en banco de preguntas |
| | |
| **2. PRESENTACIÓN DE EXÁMENES** | 🔲 **Opción C: Formulario Manual** (NUEVO) |
| ✅ `ClsEstudiante.js` interactivo | - Docente escribe pregunta por pregunta |
| ✅ Temporizador por pregunta y total | - Campos: enunciado, 4 opciones, respuesta correcta |
| ✅ Retroalimentación inmediata | - Dificultad, puntos, explicación |
| ✅ Explicación de respuesta correcta | - Se guarda directo en JSON |
| ✅ Guardado en `resultados_examen` | - Sin IA, sin PDF |
| ✅ Detalle en `respuestas_examen_detalle` | |
| ✅ Calificación automática (0-5, S/A/B/b/I) | 🔲 **Opción D: Contexto Multimodal** (NUEVO) |
| ✅ Dashboard estudiante | - Docente sube imagen/video como contexto |
| | - Se adjunta a la pregunta (antes del enunciado) |
| | - Soporte para: imágenes, videos, audio |
| | - Almacenamiento en cloud/local |
| | - Referencia en JSON: `{"tipo": "imagen", "src": "..."}` |
| **3. MODELOS DE BD** | |
| ✅ `examenes` (contenido_json JSONB) | **3. ANÁLISIS IA POST-EXAMEN** (NUEVO) |
| ✅ `preguntas` (banco reutilizable) | 🔲 Después de presentar examen: |
| ✅ `resultados_examen` | - IA analiza respuestas del estudiante |
| ✅ `respuestas_examen_detalle` | - Detecta fortalezas (temas dominados) |
| ✅ `usuarios` + `estudiantes` | - Detecta debilidades (temas débiles) |
| | - Genera plan de acción personalizado |
| | - Docente puede orientar/ajustar el plan |
| | - Estudiante recibe informe con recomendaciones |
| **4. RUTAS FLASK** | |
| ✅ `examen_routes.py` (API + CRUD docente) | **4. INTEGRACIÓN PENDIENTE** |
| ✅ `estudiante_routes.py` (gestión + exámenes) |  Asegurar que IA funcione con ClsEstudiante.js |
| |  Adaptar formato `contenido_json` al que espera JS |
| | 🔧 Verificar claves: `pregunta`, `respuesta`, `opciones` |
| | |
| **5. TEMPLATES** | **5. NUEVOS TEMPLATES NECESARIOS** |
| ✅ `crear_examen_ia.html` | 🔲 `subir_cuestionario_icfes.html` (Opción B) |
| ✅ `preview_ia.html` | 🔲 `crear_pregunta_manual.html` (Opción C) |
| ✅ `listar_examenes.html` | 🔲 `subir_contexto_multimodal.html` (Opción D) |
| ✅ `ver_examen.html` | 🔲 `informe_fortalezas_debilidades.html` (Análisis IA) |
| ✅ `editar_examen.html` | 🔲 `plan_accion_estudiante.html` |
| ✅ `examen_estudiante.html` | |
| ✅ `dashboard_estudiante.html` | |
| ✅ `mis_resultados.html` | |

---

##  **PRIORIZACIÓN SUGERIDA**

### **FASE 1: Integración (URGENTE)**
1. ✅ Adaptar `obtener_json_examen` para que IA funcione con ClsEstudiante.js
2. ✅ Probar flujo completo: crear → presentar → calificar

### **FASE 2: Banco de Preguntas (ALTA)**
3. 🔲 Opción B: Subida de cuestionario ICFES (parser automático)
4. 🔲 Opción C: Formulario manual de creación
5. 🔲 Opción D: Contexto multimodal (imágenes/videos)

### **FASE 3: Análisis IA (MEDIA)**
6.  Análisis de fortalezas/debilidades post-examen
7. 🔲 Plan de acción personalizado
8. 🔲 Dashboard docente con estadísticas

---

## 💡 **MI OPINIÓN**

**Excelente propuesta.** Lo que planteas es un **sistema completo de evaluación adaptativa**:

1. **Múltiples formas de crear preguntas** → Flexibilidad total para el docente
2. **Contexto multimodal** → Exámenes más ricos y realistas (tipo ICFES/Saber)
3. **Análisis IA post-examen** → No solo calificar, sino **orientar** al estudiante

Esto convierte a SistPROF en una **plataforma de aprendizaje adaptativo**, no solo un gestor de exámenes.

---

**¿Por cuál quieres empezar?** 

**Mi recomendación:** 
1. **Primero** integra la IA con ClsEstudiante.js (FASE 1)
2. **Luego** agrega el formulario manual (Opción C) - es el más simple
3. **Después** el parser de cuestionario ICFES (Opción B)
4. **Finalmente** el análisis IA post-examen

**¿De acuerdo?** 