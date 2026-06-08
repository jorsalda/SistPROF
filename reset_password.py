# cambiar_password.py
from werkzeug.security import generate_password_hash
import psycopg2
from sqlalchemy import create_engine, text

# Tu conexión de Supabase (reemplaza ****** con tu contraseña real)
DATABASE_URL = "postgresql://postgres.spliytdoiaolqxcepvos:Je03Sh26%23%23%23%24@aws-1-us-west-2.pooler.supabase.com:6543/postgres"


def cambiar_contraseña():
    try:
        # Conectar a Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        print("✅ Conectado a Supabase")

        # Nueva contraseña para jor@jorj.or
        nueva_password = "123456"  # Cámbiala si quieres
        nuevo_hash = generate_password_hash(nueva_password, method='pbkdf2:sha256:600000')

        # Actualizar
        cursor.execute(
            "UPDATE usuarios SET password_hash = %s WHERE email = %s",
            (nuevo_hash, "jor@jor")
        )

        if cursor.rowcount > 0:
            conn.commit()
            print(f"✅ Contraseña cambiada exitosamente!")
            print(f"📧 Email: jor@jor")
            print(f"🔑 Nueva contraseña: {nueva_password}")
        else:
            print(f"❌ No se encontró el email: jor@jorj.or")

            # Mostrar qué emails existen
            cursor.execute("SELECT id, email FROM usuarios")
            print("\n📋 Emails registrados:")
            for uid, email in cursor.fetchall():
                print(f"   {uid} - {email}")

        cursor.close()
        conn.close()

    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Verifica:")
        print("1. Que el ****** sea tu contraseña real de Supabase")
        print("2. Que la tabla se llame 'usuarios' (no 'usuaris')")
        print("3. Que el email sea exactamente 'jor@jorj.or'")


if __name__ == "__main__":
    cambiar_contraseña()