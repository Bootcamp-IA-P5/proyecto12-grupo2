import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

POSTGRES_DB = os.getenv("POSTGRES_DB", None)
POSTGRES_USER = os.getenv("POSTGRES_USER", None)
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", None)
POSTGRES_HOST = os.getenv("POSTGRES_HOST", None)
POSTGRES_PORT = os.getenv("POSTGRES_PORT", None)

YOLO_MODEL_ORG = '/workspaces/proyecto12-grupo2/models/models_org/weights/best.pt'