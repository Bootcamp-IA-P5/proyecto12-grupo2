#!/usr/bin/env python
import sys


# Agregar el directorio de proyecto al path
sys.path.insert(0, '/workspaces/proyecto12-grupo2')

if __name__ == "__main__":
    from src.api import app
    import uvicorn

    print("🚀 Iniciando KUMO VISION API...")
    print("📍 http://localhost:8000")
    print("📚 Documentación: http://localhost:8000/docs")

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
