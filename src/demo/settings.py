import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Define the base directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Logging configuration
LOG_FILE_NAME = os.getenv("LOG_FILE_NAME","kumo.log")
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")
LOG_BASE_DIR = os.getenv("LOG_BASE_DIR", "log")

# Database configuration
POSTGRES_DB = os.getenv("POSTGRES_DB", None)
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", None)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", None)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# YOLO model paths
YOLO_MODEL_ORG = os.path.join(BASE_DIR, 'models/models_org/weights/best.pt')