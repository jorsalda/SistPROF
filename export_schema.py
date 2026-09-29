import sys
from app import create_app
from app.extensions import db
from sqlalchemy.schema import CreateTable

# Inicializa la aplicación Flask
app = create_app()

with app.app_context():
    # Importar los modelos explícitamente para asegurar que se registren en la Metadata
    import app.models  # noqa: F401

    print("-- ===============================================")
    print("-- ESTRUCTURA EXACTA DE MODELOS (SQLAlchemy DDL)")
    print("-- ===============================================\n")

    for table in db.metadata.sorted_tables:
        print(f"-- Tabla: {table.name}")
        print(str(CreateTable(table).compile(db.engine)).strip() + ";\n")