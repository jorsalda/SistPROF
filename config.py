# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave_super_segura'
    
    # Configuración de base de datos PostgreSQL
    # En desarrollo: usa DATABASE_URL del archivo .env
    # En Render: usa DATABASE_URL de las variables de entorno de Render
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # SQLAlchemy requiere 'postgresql://' en lugar de 'postgres://'
        if database_url.startswith('postgres://'):
            database_url = database_url.replace('postgres://', 'postgresql://', 1)
        SQLALCHEMY_DATABASE_URI = database_url
    else:
        # Fallback: tu configuración local actual (PostgreSQL local)
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:jes8026@localhost:5432/permisos'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
