import os
import json
import logging
from google import genai
from google.genai import types

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Lista de modelos estables disponibles (en orden de prioridad)
MODELOS_DISPONIBLES = [
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.0-flash",
    "gemini-flash-latest",
    "gemini-pro-latest"
]


def generar_preguntas_json(texto, materia, grado, cantidad):
    """
    Genera preguntas tipo ICFES en formato JSON usando Google Gemini.
    Incluye un sistema de fallback para probar múltiples modelos si uno falla.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    Eres un experto docente en Colombia, especializado en pruebas tipo ICFES/Saber.
    Tu tarea es generar {cantidad} preguntas de selección múltiple con única respuesta sobre el siguiente tema de {materia} para estudiantes de {grado}.

    CONTEXTO DEL MATERIAL DE ESTUDIO:
    {texto}

    REGLAS ESTRICTAS:
    1. Devuelve SOLO un objeto JSON válido. NO incluyas markdown (```json), NO incluyas texto antes o después del JSON.
    2. El JSON debe tener esta estructura exacta:
    {{
      "preguntas": [
        {{
          "numero": 1,
          "texto": "Enunciado claro y contextualizado de la pregunta",
          "opciones": {{
            "A": "Opción A",
            "B": "Opción B",
            "C": "Opción C",
            "D": "Opción D"
          }},
          "respuesta_correcta": "A",
          "dificultad": "media",
          "explicacion": "Explicación breve de por qué es la respuesta correcta"
        }}
      ]
    }}
    3. Las opciones deben ser plausibles y la respuesta correcta debe estar justificada en el contexto.
    4. No inventes información que no esté en el contexto o en el conocimiento general de la materia.
    """

    ultimo_error = None

    # Intentar con cada modelo hasta que uno funcione
    for modelo in MODELOS_DISPONIBLES:
        try:
            logger.info(f"Intentando generar preguntas con el modelo: {modelo}")

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )

            # Limpiar posible markdown que la IA a veces agrega a pesar de las instrucciones
            texto_respuesta = response.text.strip()
            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]
            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]

            texto_respuesta = texto_respuesta.strip()

            # Validar que sea JSON
            datos = json.loads(texto_respuesta)
            logger.info(f"✅ Éxito con el modelo: {modelo}")
            return datos

        except json.JSONDecodeError as e:
            ultimo_error = f"El modelo {modelo} no devolvió JSON válido: {e}. Respuesta: {response.text[:200]}"
            logger.warning(ultimo_error)
            continue  # Intentar con el siguiente modelo
        except Exception as e:
            ultimo_error = f"Error con el modelo {modelo}: {str(e)}"
            logger.warning(ultimo_error)
            continue  # Intentar con el siguiente modelo

    # Si todos los modelos fallaron
    raise Exception(f"No se pudo generar el examen. Último error: {ultimo_error}")


# ============================================================
# PLAN MAESTRO: PLANILLA INTELIGENTE SISTPROF - PASO 5.3
# Agregar esta función a tu ia_services.py existente
# ============================================================

def generar_analisis_pedagogico(contexto_notas):
    """
    Analiza el desempeño estudiantil y genera fortalezas, debilidades y plan de apoyo.
    Reutiliza el mismo cliente, modelos y fallback de generar_preguntas_json.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("No se encontró la variable de entorno GEMINI_API_KEY")

    client = genai.Client(api_key=api_key)

    # Construir contexto legible para la IA desde las notas
    notas_texto = "\n".join([
        f"- Competencia: {n['competencia']} [{n['codigo']}] | Indicador: {n['indicador']} | Nota: {n['nota']}"
        for n in contexto_notas
    ])

    prompt = f"""
    Eres un experto pedagogo colombiano especializado en evaluación por competencias.
    Analiza las siguientes notas de un estudiante y genera un informe pedagógico estructurado.

    DATOS DEL ESTUDIANTE:
    {notas_texto}

    REGLAS ESTRICTAS:
    1. Devuelve SOLO un objeto JSON válido. NO incluyas markdown (```json), NO incluyas texto antes o después.
    2. El JSON debe tener esta estructura exacta:
    {{
      "fortalezas": [
        "Descripción clara de una fortaleza basada en notas altas (>=4.0)",
        "Otra fortaleza específica con referencia al código de competencia"
      ],
      "debilidades": [
        "Descripción clara de una debilidad basada en notas bajas (<3.0)",
        "Otra debilidad específica con referencia al código de indicador"
      ],
      "plan_apoyo": "Texto detallado (máximo 3 párrafos) con estrategias pedagógicas concretas, actividades sugeridas y recursos recomendados para mejorar las debilidades identificadas. Debe ser práctico y aplicable en contexto escolar colombiano."
    }}
    3. Las fortalezas y debilidades deben estar DIRECTAMENTE respaldadas por las notas proporcionadas. No inventes.
    4. El plan de apoyo debe ser accionable, específico y alineado con el currículo por competencias.
    5. Usa lenguaje profesional pero accesible para docentes.
    """

    ultimo_error = None

    # Reutilizar EXACTAMENTE la misma lógica de fallback de modelos
    for modelo in MODELOS_DISPONIBLES:
        try:
            logger.info(f"Intentando análisis pedagógico con modelo: {modelo}")

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.3,  # Menor temperatura para análisis más preciso
                    response_mime_type="application/json"
                )
            )

            # Limpieza de markdown (misma lógica que generar_preguntas_json)
            texto_respuesta = response.text.strip()
            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]
            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]
            texto_respuesta = texto_respuesta.strip()

            # Validar JSON
            datos = json.loads(texto_respuesta)

            # Validar estructura mínima
            if not all(k in datos for k in ['fortalezas', 'debilidades', 'plan_apoyo']):
                raise ValueError("Respuesta IA no tiene estructura esperada")

            logger.info(f"✅ Análisis pedagógico exitoso con modelo: {modelo}")
            return datos

        except json.JSONDecodeError as e:
            ultimo_error = f"Modelo {modelo} no devolvió JSON válido: {e}"
            logger.warning(ultimo_error)
            continue
        except Exception as e:
            ultimo_error = f"Error con modelo {modelo}: {str(e)}"
            logger.warning(ultimo_error)
            continue

    raise Exception(f"No se pudo generar análisis pedagógico. Último error: {ultimo_error}")