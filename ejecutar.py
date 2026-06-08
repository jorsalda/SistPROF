# diagnosticar_login.py
import psycopg2
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')

print("=" * 50)
print("🔍 DIAGNÓSTICO DE LOGIN")
print("=" * 50)

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 1. Obtener el usuario
email_prueba = "jor@jor.jor"
cursor.execute("SELECT id, email, password_hash FROM usuarios WHERE email = %s", (email_prueba,))
resultado = cursor.fetchone()

if not resultado:
    print(f"❌ ERROR: El email '{email_prueba}' NO EXISTE en la BD")
else:
    id_usuario, email, hash_almacenado = resultado
    print(f"✅ Usuario encontrado:")
    print(f"   ID: {id_usuario}")
    print(f"   Email: {email}")
    print(f"   Hash: {hash_almacenado[:60]}...")

    # 2. Probar la contraseña "123456"
    contraseña_prueba = "123456"
    es_valida = check_password_hash(hash_almacenado, contraseña_prueba)

    print(f"\n🔐 Probando contraseña '{contraseña_prueba}':")
    print(f"   {'✅ ES VÁLIDA' if es_valida else '❌ NO ES VÁLIDA'}")

    # 3. Si no es válida, probar a generar un nuevo hash
    if not es_valida:
        print("\n⚠️ La contraseña '123456' NO funciona con el hash actual")
        print("   Vamos a generar un hash NUEVO desde cero con el método que usa tu app...")

        from werkzeug.security import generate_password_hash

        # Ver qué método usa tu app
        print("\n📋 Generando hash con diferentes métodos:")

        metodos = [
            ('pbkdf2:sha256:600000', 'pbkdf2:sha256:600000'),
            ('pbkdf2:sha256:260000', 'pbkdf2:sha256:260000'),
            ('scrypt', 'scrypt'),
            (None, 'default')
        ]

        for nombre, metodo in metodos:
            try:
                if metodo is None:
                    nuevo_hash = generate_password_hash("123456")
                else:
                    nuevo_hash = generate_password_hash("123456", method=metodo)
                print(f"   {nombre}: {nuevo_hash[:50]}...")
            except:
                print(f"   {nombre}: ❌ Error")

        # 4. Actualizar con el método más compatible
        print("\n🔄 Actualizando la contraseña...")
        nuevo_hash_final = generate_password_hash("123456")  # método default
        cursor.execute("UPDATE usuarios SET password_hash = %s WHERE email = %s",
                       (nuevo_hash_final, email_prueba))
        conn.commit()
        print(f"✅ Hash actualizado!")
        print(f"🔑 Nueva contraseña: 123456")
        print(f"\n✨ AHORA SÍ deberías poder iniciar sesión")

cursor.close()
conn.close()