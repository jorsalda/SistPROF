from dotenv import load_dotenv

# Cargar variables de entorno ANTES de importar la app
load_dotenv()

from app import create_app

app = create_app()

if __name__ == '__main__':
    # ✅ Solo para local, Fly.io usa gunicorn
    app.run(host='0.0.0.0', port=5000, debug=False)