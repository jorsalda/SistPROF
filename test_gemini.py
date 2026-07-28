import google.generativeai as genai
import os

# Cargar la clave
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("GEMINI_API_KEY")
print(f"API Key: {api_key[:20]}..." if api_key else "NO HAY API KEY")

if not api_key:
    print("❌ Error: No se encontró GEMINI_API_KEY en el archivo .env")
    exit()

genai.configure(api_key=api_key)

print("\n🔍 Buscando modelos disponibles...\n")

try:
    models = genai.list_models()
    available_models = []

    for model in models:
        if 'generateContent' in model.supported_generation_methods:
            available_models.append(model.name)
            print(f"✅ {model.name}")

    if not available_models:
        print("❌ No se encontraron modelos disponibles para generar contenido")
        print("\n💡 Solución: Tu API Key puede no estar activada correctamente.")
        print("Ve a https://aistudio.google.com/app/apikey y verifica el estado de tu clave.")
    else:
        print(f"\n📋 Total de modelos disponibles: {len(available_models)}")

except Exception as e:
    print(f" Error al listar modelos: {e}")
    print("\n💡 Posibles causas:")
    print("1. La API Key es inválida")
    print("2. No has habilitado la API de Gemini en Google Cloud Console")
    print("3. Tu cuenta tiene restricciones regionales")