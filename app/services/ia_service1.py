import json
from flask import current_app
from google import genai
from google.genai import types


def configurar_ia():
    """Crea el cliente de Gemini."""
    api_key = current_app.config.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY no está configurada.")
    return genai.Client(api_key=api_key)


def generar_preguntas_json(texto_documento, materia, grado, cantidad=5):
    """Genera preguntas tipo ICFES en formato JSON."""

    client = configurar_ia()

    # ✅ Modelos confirmados disponibles (del test que ejecutaste)
    modelos_a_probar = [
        "gemini-2.0-flash",  # ✅ Confirmado disponible
        "gemini-pro-latest",  # ✅ Confirmado disponible
        "gemini-flash-latest",  # ✅ Confirmado disponible
        "gemini-2.0-flash-exp",  # Experimental
    ]

    texto_corto = texto_documento[:3000] if texto_documento else "Texto no disponible"

    prompt = f"""
Eres un docente experto en preguntas tipo ICFES.
Genera {cantidad} preguntas de selección múltiple sobre {materia} para grado {grado}.

Material: {texto_corto}

Devuelve SOLO este JSON (sin markdown):
{{
  "preguntas":[
    {{
      "numero":1,
      "texto":"Pregunta",
      "opciones":{{"A":"A","B":"B","C":"C","D":"D"}},
      "respuesta_correcta":"A",
      "explicacion":"Explicación",
      "dificultad":"media"
    }}
  ]
}}
"""

    ultimo_error = None

    for modelo in modelos_a_probar:
        try:
            print(f"🤖 Probando: {modelo}")

            response = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    response_mime_type="application/json"
                )
            )

            texto = response.text.strip()
            resultado = json.loads(texto)

            if "preguntas" in resultado:
                print(f"✅ Éxito con: {modelo}")
                return resultado

        except Exception as e:
            error_msg = str(e)
            print(f"⚠️  {modelo} falló: {error_msg[:80]}")
            ultimo_error = e
            # Continuar con el siguiente modelo
            continue

    # Si ningún modelo funcionó
    raise Exception(f"Ningún modelo disponible. Último error: {str(ultimo_error)}")