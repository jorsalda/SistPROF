import os
from dotenv import load_dotenv
from google import genai

# 1. Cargar las variables del archivo .env
load_dotenv()

# 2. Obtener la API Key
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: No se encontró la GEMINI_API_KEY en tu archivo .env")
else:
    print("✅ API Key encontrada. Consultando modelos disponibles...\n")
    try:
        client = genai.Client(api_key=api_key)
        print("Modelos disponibles:")
        for model in client.models.list():
            print(f"- {model.name}")
    except Exception as e:
        print(f"❌ Error al conectar con la API de Google: {e}")