from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from ultralytics import YOLO
import base64
from io import BytesIO
from PIL import Image
import os
from pathlib import Path

# Inicializar FastAPI
app = FastAPI(title="KUMO VISION API", version="1.0.0")

# Configurar CORS para que el frontend pueda hacer requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cargar modelo YOLO
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = os.path.join(BASE_DIR, 'models/models_org/weights/best.pt')

print(f"Buscando modelo en: {MODEL_PATH}")
print(f"Modelo existe: {os.path.exists(MODEL_PATH)}")

# Intentar cargar el modelo
try:
    model = YOLO(MODEL_PATH)
    print("✅ Modelo YOLO cargado exitosamente")
except Exception as e:
    print(f"⚠️ Error al cargar modelo: {e}")
    # Usar un modelo preentrenado como fallback
    model = YOLO('yolov8n.pt')
    print("📥 Usando modelo preentrenado YOLOv8n como fallback")

# Mapeo de clases a nombres amigables (puedes ajustar esto)
class_names_mapping = {
    0: 'Apple',
    1: 'Nike',
    2: 'Google',
    3: 'Microsoft',
    4: 'Amazon',
    5: 'Facebook',
    6: 'Tesla',
    7: 'Twitter',
    8: 'Instagram',
    9: 'TikTok'
}


@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "KUMO VISION API",
        "version": "1.0.0",
        "endpoints": [
            "/detect/image - POST - Detectar logos en una imagen",
            "/detect/base64 - POST - Detectar logos desde base64",
            "/health - GET - Estado del servidor"
        ]
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "model_path": MODEL_PATH
    }


@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """
    Detectar logos en una imagen subida
    """
    try:
        # Leer imagen
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert('RGB')
        image_np = np.array(image)

        # Convertir RGB a BGR para OpenCV
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Inferencia
        results = model.predict(image_bgr, conf=0.5, verbose=False)

        # Procesar resultados
        detections = []
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Obtener nombre de clase
                class_name = model.names.get(cls_id, f"Class {cls_id}")

                # Crear objeto de detección
                detection = {
                    "class_id": cls_id,
                    "class_name": class_name,
                    "confidence": round(confidence * 100, 2),
                    "bbox": [float(x) for x in box.xyxy[0].tolist()]
                }
                detections.append(detection)

        # Ordenar por confianza (mayor primero)
        detections = sorted(
            detections, key=lambda x: x['confidence'], reverse=True)

        return {
            "status": "success",
            "total_detections": len(detections),
            "detections": detections,
            "image_size": {
                "width": image.width,
                "height": image.height
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error procesando imagen: {str(e)}")


@app.post("/detect/base64")
async def detect_base64(data: dict):
    """
    Detectar logos desde imagen en base64
    Espera: {"image": "base64_string"}
    """
    try:
        base64_string = data.get('image')
        if not base64_string:
            raise ValueError("No image data provided")

        # Decodificar base64
        image_data = base64.b64decode(base64_string)
        image = Image.open(BytesIO(image_data)).convert('RGB')
        image_np = np.array(image)

        # Convertir RGB a BGR para OpenCV
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Inferencia
        results = model.predict(image_bgr, conf=0.5, verbose=False)

        # Procesar resultados
        detections = []
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])

                # Obtener nombre de clase
                class_name = model.names.get(cls_id, f"Class {cls_id}")

                # Crear objeto de detección
                detection = {
                    "class_id": cls_id,
                    "class_name": class_name,
                    "confidence": round(confidence * 100, 2),
                    "bbox": [float(x) for x in box.xyxy[0].tolist()]
                }
                detections.append(detection)

        # Ordenar por confianza (mayor primero)
        detections = sorted(
            detections, key=lambda x: x['confidence'], reverse=True)

        return {
            "status": "success",
            "total_detections": len(detections),
            "detections": detections,
            "image_size": {
                "width": image.width,
                "height": image.height
            }
        }

    except Exception as e:
        raise HTTPException(
            status_code=400, detail=f"Error procesando imagen: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
