# test_conexion.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')
print(f"Intentando conectar a: {DATABASE_URL}")

try:
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ ¡Conexión exitosa a PostgreSQL local!")

    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    version = cursor.fetchone()
    print(f"📦 Versión PostgreSQL: {version[0][:50]}...")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")