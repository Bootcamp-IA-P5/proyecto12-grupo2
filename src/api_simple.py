from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
sys.path.insert(0, '/workspaces/proyecto12-grupo2')

print("🔧 Cargando FastAPI...")
app = FastAPI(title="KUMO VISION API", version="1.0.0")

print("⚙️  Configurando CORS...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🤖 Cargando modelo YOLO (esto puede tardar)...")
try:
    from ultralytics import YOLO
    import os
    from pathlib import Path

    BASE_DIR = Path('/workspaces/proyecto12-grupo2')
    MODEL_PATH = os.path.join(BASE_DIR, 'models/models_org/weights/best.pt')

    print(f"   Ruta: {MODEL_PATH}")
    print(f"   Existe: {os.path.exists(MODEL_PATH)}")

    if os.path.exists(MODEL_PATH):
        model = YOLO(MODEL_PATH)
        print("   ✅ Modelo cargado exitosamente")
    else:
        print("   ⚠️  Modelo no encontrado, usando YOLOv8n")
        model = YOLO('yolov8n.pt')
except Exception as e:
    print(f"   ❌ Error: {e}")
    model = None

print("📡 Registrando endpoints...")


@app.get("/")
async def root():
    return {
        "status": "online",
        "app": "KUMO VISION API",
        "version": "1.0.0"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    """Detectar logos en una imagen subida"""
    try:
        from PIL import Image
        from io import BytesIO
        import numpy as np
        import cv2

        print(f"📸 Procesando imagen: {file.filename}")

        # Leer imagen
        contents = await file.read()
        image = Image.open(BytesIO(contents)).convert('RGB')
        image_np = np.array(image)

        # Convertir RGB a BGR
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

        # Inferencia
        results = model.predict(image_bgr, conf=0.5, verbose=False)

        # Procesar detecciones
        detections = []
        if len(results[0].boxes) > 0:
            for box in results[0].boxes:
                cls_id = int(box.cls[0])
                confidence = float(box.conf[0])
                class_name = model.names.get(cls_id, f"Class {cls_id}")

                detection = {
                    "class_id": cls_id,
                    "class_name": class_name,
                    "confidence": round(confidence * 100, 2),
                    "bbox": [float(x) for x in box.xyxy[0].tolist()]
                }
                detections.append(detection)

        # Ordenar por confianza
        detections = sorted(
            detections, key=lambda x: x['confidence'], reverse=True)

        print(f"✅ Detectadas {len(detections)} objetos")

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
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("\n🚀 Iniciando servidor...")
    print("📍 http://0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
