# 📋 RESUMEN CONCRETO: LAS 3 VÍAS DE CREACIÓN DE PREGUNTAS EN SistPROF

| **VÍA DE CREACIÓN** | **FLUJO TÉCNICO Y ESTADO ACTUAL** |
| :--- | :--- |
| **1. Generación con IA (Ya Funcional)** | Docente sube PDF/DOCX → `document_service.py` extrae texto → `ia_service.py` llama a Gemini con fallback de modelos → Devuelve JSON estructurado → Docente revisa en `preview_ia.html` → Se guarda en `examenes.contenido_json` y tabla `preguntas`. **Estado:** ✅ Completado y operativo. |
| **2. Creación Manual Pregunta por Pregunta (Pendiente - Opción C)** | Docente accede a formulario `/crear-pregunta-manual` → Ingresa: enunciado, 4 opciones (A/B/C/D), respuesta correcta, dificultad, puntos, explicación → Backend valida campos obligatorios → Construye objeto JSON estándar → Guarda directamente en tabla `preguntas` (banco) sin pasar por IA → Permite asignar a examen existente o crear nuevo. **Ventaja:** Control total, sin costo de tokens, ideal para preguntas específicas o de dominio propio. **Estado:** 🔲 Por desarrollar. Requiere: ruta Flask, template con validación JS, endpoint POST. |
| **3. Subida de Cuestionario ICFES Estructurado (Pendiente - Opción B)** | Docente sube PDF/DOCX con preguntas YA formuladas tipo ICFES (formato: "Pregunta X", opciones A-D, "Respuesta correcta: X") → Parser personalizado (`parser_icfes.py`) detecta patrones mediante regex o NLP básico → Extrae: número, texto, opciones, respuesta, explicación → Convierte a JSON estándar → Muestra preview para validación docente → Guarda en banco de preguntas. **Reto técnico:** El parser debe ser robusto ante variaciones de formato (negritas, viñetas, saltos de línea). **Estado:** 🔲 Por desarrollar. Requiere: motor de parsing, reglas de detección, template de confirmación. |

### 💡 INTEGRACIÓN CON EL SISTEMA EXISTENTE:
-   **Todas las vías alimentan la misma tabla `preguntas`** con estructura uniforme (`texto`, `opciones`, `respuesta_correcta`, `explicacion`, `dificultad`).
-   **El examen final siempre se construye desde el banco**, mezclando preguntas de cualquier origen (IA + manual + parser).
-   **ClsEstudiante.js no distingue el origen**: solo consume el JSON estandarizado vía `/api/examen/<id>/json`.
-   **Prioridad sugerida:** Opción C (manual) primero por simplicidad; Opción B (parser) después por complejidad técnica.

### ⚠️ NOTA CRÍTICA PARA PRODUCCIÓN:
La **Opción C (manual)** es la más segura para producción inmediata: no depende de IA, no tiene costos variables, y garantiza disponibilidad 24/7 incluso si Google falla. La **Opción B (parser)** requiere testing exhaustivo con documentos reales antes de liberar, ya que errores de parsing generarían preguntas corruptas.