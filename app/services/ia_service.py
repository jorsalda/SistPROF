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