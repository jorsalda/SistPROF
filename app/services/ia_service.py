import os
import json
import logging

from google import genai
from google.genai import types


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Modelos actuales
MODELOS_DISPONIBLES = [
    "gemini-3.6-flash",
    "gemini-3.5-flash",
]


def _get_client():
    """Crea el cliente de Gemini usando GEMINI_API_KEY."""

    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("Falta variable GEMINI_API_KEY")

    return genai.Client(api_key=api_key)


def generar_preguntas_json(texto, materia, grado, cantidad):

    client = _get_client()

    prompt = f"""
Eres un experto docente en educación colombiana y en elaboración de
preguntas tipo ICFES/Saber 11.

Genera {cantidad} preguntas de selección múltiple sobre:

Materia: {materia}
Grado: {grado}

CONTEXTO DEL MATERIAL:
{texto}

REGLAS:

1. Genera exactamente {cantidad} preguntas.
2. Cada pregunta debe tener cuatro opciones: A, B, C y D.
3. Debe existir una única respuesta correcta.
4. Las preguntas deben estar relacionadas con el material suministrado.
5. Deben ser apropiadas para estudiantes de {grado}.
6. Incluye una explicación de la respuesta correcta.
7. Devuelve ÚNICAMENTE JSON válido.
8. No incluyas texto antes ni después del JSON.

Estructura exacta:

{{
    "preguntas": [
        {{
            "numero": 1,
            "texto": "Texto de la pregunta",
            "opciones": {{
                "A": "Opción A",
                "B": "Opción B",
                "C": "Opción C",
                "D": "Opción D"
            }},
            "respuesta_correcta": "A",
            "dificultad": "media",
            "explicacion": "Explicación de la respuesta"
        }}
    ]
}}
"""

    ultimo_error = None

    for modelo in MODELOS_DISPONIBLES:

        try:

            logger.info(f"Intentando modelo: {modelo}")

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            texto_respuesta = response.text.strip()

            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]

            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]

            datos = json.loads(texto_respuesta)

            if "preguntas" not in datos:
                raise ValueError("La respuesta no contiene 'preguntas'")

            logger.info(f"ÉXITO con modelo: {modelo}")

            return datos

        except Exception as e:

            ultimo_error = str(e)

            logger.warning(
                f"Falló {modelo}: {ultimo_error[:300]}"
            )

            continue

    raise Exception(
        f"Fallo total IA: {ultimo_error}"
    )


def generar_analisis_pedagogico(contexto_notas):

    client = _get_client()

    notas_texto = "\n".join(
        [
            f"- {n['competencia']} "
            f"[{n['codigo']}] | "
            f"{n['indicador']} | "
            f"Nota: {n['nota']}"
            for n in contexto_notas
        ]
    )

    prompt = f"""
Eres un experto pedagogo colombiano.

Analiza las siguientes notas:

{notas_texto}

Devuelve únicamente JSON válido con esta estructura:

{{
    "fortalezas": [],
    "debilidades": [],
    "plan_apoyo": []
}}
"""

    ultimo_error = None

    for modelo in MODELOS_DISPONIBLES:

        try:

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            texto_respuesta = response.text.strip()

            if texto_respuesta.startswith("```json"):
                texto_respuesta = texto_respuesta[7:]

            if texto_respuesta.endswith("```"):
                texto_respuesta = texto_respuesta[:-3]

            datos = json.loads(texto_respuesta)

            if not all(
                k in datos
                for k in [
                    "fortalezas",
                    "debilidades",
                    "plan_apoyo"
                ]
            ):
                raise ValueError("JSON incompleto")

            logger.info(
                f"Análisis exitoso con modelo: {modelo}"
            )

            return datos

        except Exception as e:

            ultimo_error = str(e)

            logger.warning(
                f"Falló análisis con {modelo}: "
                f"{ultimo_error[:300]}"
            )

            continue

    raise Exception(
        f"Fallo análisis IA: {ultimo_error}"
    )