from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="KUMO VISION API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "online", "app": "KUMO VISION API"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/detect/image")
async def detect_image(file: UploadFile = File(...)):
    # Lee el archivo pero no lo procesa
    await file.read()

    return {
        "status": "success",
        "total_detections": 3,
        "detections": [
            {"class_id": 0, "class_name": "Instagram",
                "confidence": 99.2, "bbox": [0, 0, 100, 100]},
            {"class_id": 1, "class_name": "Apple",
                "confidence": 98.5, "bbox": [100, 0, 200, 100]},
            {"class_id": 2, "class_name": "Nike",
                "confidence": 97.8, "bbox": [200, 0, 300, 100]}
        ],
        "image_size": {"width": 640, "height": 480}
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
