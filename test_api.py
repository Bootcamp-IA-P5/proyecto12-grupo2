#!/usr/bin/env python
"""Script de prueba rápido del API"""
from fastapi.testclient import TestClient
from src.api import app
import sys
import json
from io import BytesIO
from PIL import Image
import numpy as np

# Importar directamente
sys.path.insert(0, '/workspaces/proyecto12-grupo2')

# Crear una imagen de prueba
print("Creando imagen de prueba...")
img = Image.new('RGB', (640, 480), color='red')
img_bytes = BytesIO()
img.save(img_bytes, format='JPEG')
img_bytes.seek(0)

# Simular una petición POST

client = TestClient(app)

print("\n✅ Probando endpoint /")
response = client.get("/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n✅ Probando endpoint /health")
response = client.get("/health")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")

print("\n✅ Probando endpoint /detect/image")
response = client.post(
    "/detect/image",
    files={"file": ("test.jpg", img_bytes, "image/jpeg")}
)
print(f"Status: {response.status_code}")
if response.status_code == 200:
    print(f"Response: {response.json()}")
else:
    print(f"Error: {response.text}")
