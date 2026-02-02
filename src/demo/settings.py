import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

BASE_DIR = Path(__file__).resolve().parent.parent.parent

POSTGRES_DB = os.getenv("POSTGRES_DB", None)
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", None)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", None)

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# YOLO model paths
YOLO_MODEL_ORG = os.path.join(BASE_DIR, 'models/models_org_2/weights/best.pt')