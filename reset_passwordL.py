# cambiar_password_local.py
import os
import psycopg2
from werkzeug.security import generate_password_hash
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

try:
    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    # Primero, ver qué usuarios existen
    cursor.execute("SELECT id, email FROM usuarios")
    usuarios = cursor.fetchall()

    print("📋 Usuarios en BD local:")
    for uid, email in usuarios:
        print(f"   ID: {uid} | Email: {email}")

    # Cambiar contraseña
    nueva_password = "123456"
    nuevo_hash = generate_password_hash(nueva_password, method='pbkdf2:sha256:600000')

    cursor.execute(
        "UPDATE usuarios SET password_hash = %s WHERE email = %s",
        (nuevo_hash, "jes@jes.jes")
    )

    if cursor.rowcount > 0:
        conn.commit()
        print(f"\n✅ ¡Contraseña cambiada!")
        print(f"   Email: jes@jes.jes")
        print(f"   Nueva contraseña: {nueva_password}")
    else:
        print(f"\n❌ No se encontró el email: jes@jes.jes")
        print("💡 Los emails disponibles son los que ves arriba")

    cursor.close()
    conn.close()

except Exception as e:
    print(f"❌ Error: {e}")