import sys
import os

# Añadir la ruta del proyecto al path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app

app = create_app()
