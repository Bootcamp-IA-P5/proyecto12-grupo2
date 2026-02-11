# 🚀 Guía para Entrenar el Modelo en Google Colab

## ✅ Ventajas de entrenar en Colab
- **GPU T4 gratis** (~15x más rápido que CPU)
- **Entrenamiento**: 20-30 minutos vs 12+ horas en local
- No consume recursos de tu Mac

---

## 📋 Pasos para entrenar en Google Colab

### 1. Preparar el Dataset

**Ya descargado:** Flickr Logos 27 Dataset

Necesitas subir a Google Drive:
- `flickr_logos_27_dataset.zip` (el dataset completo)
- `data.yaml` (configuración del dataset)

### 2. Abrir el Notebook en Colab

1. Ve a: https://colab.research.google.com
2. Click en **File → Upload notebook**
3. Sube tu archivo: `umit-train/train_yolo_colab.ipynb`

**O directamente desde GitHub:**
1. En Colab: **File → Open notebook → GitHub**
2. Pega la URL de tu repo: `https://github.com/Bootcamp-IA-P5/proyecto12-grupo2`
3. Selecciona tu rama y el notebook

### 3. Activar GPU en Colab

**⚠️ IMPORTANTE - Hacer antes de ejecutar:**

1. En Colab: **Runtime → Change runtime type**
2. Seleccionar: **T4 GPU**
3. Click **Save**

### 4. Ejecutar el Entrenamiento

Ejecuta las celdas en orden:

```python
# Celda 1: Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Celda 2: Instalar Ultralytics
!pip install -q ultralytics>=8.3.0

# Celda 3: Verificar GPU
!nvidia-smi

# Celda 4: Descomprimir dataset
!unzip -q /content/drive/MyDrive/flickr_logos_27_dataset.zip -d /content/dataset/

# Celda 5: ENTRENAR (20-30 min)
from ultralytics import YOLO
model = YOLO('yolo11n.pt')
results = model.train(
    data='/content/data.yaml',
    epochs=50,
    imgsz=640,
    batch=16,
    device=0,
    project='runs/detect',
    name='logos_flickr_dataset'
)
```

### 5. Descargar el Modelo Entrenado

Una vez finalizado el entrenamiento:

```python
# Copiar modelo a Google Drive
!cp /content/runs/detect/logos_flickr_dataset/weights/best.pt /content/drive/MyDrive/best.pt

# O descargarlo directamente
from google.colab import files
files.download('/content/runs/detect/logos_flickr_dataset/weights/best.pt')
```

### 6. Colocar el Modelo en el Proyecto

Después de descargarlo desde Colab:

1. Crear directorio local: `mkdir -p models/models_org/weights`
2. Copiar el archivo: Mover `best.pt` a `models/models_org/weights/`
3. Ejecutar pruebas: `python tests/model_evaluation/evaluate_model.py`

---

## 📊 Métricas esperadas

Después del entrenamiento verás:
- **mAP50**: ~0.70-0.85 (precision del modelo)
- **Precisión**: ~0.75-0.90
- **Recall**: ~0.65-0.80

---

## ⏱️ Tiempos estimados

| Hardware | Tiempo (50 epochs) |
|----------|-------------------|
| Colab T4 GPU | 20-30 minutos ✅ |
| Mac M1/M2 CPU | 8-12 horas ⚠️ |
| CPU Intel | 12+ horas ❌ |

---

## 🔧 Problemas comunes

### GPU no detectada en Colab
- **Solución**: Runtime → Change runtime type → T4 GPU → Save → Restart

### Dataset no encontrado
- **Solución**: Verifica que `flickr_logos_27_dataset.zip` esté en la raíz de tu Google Drive

### Error "data.yaml not found"
- **Solución**: Sube `data.yaml` a Google Drive (raíz)

---

## 📚 Recursos adicionales

- [Documentación Ultralytics YOLO](https://docs.ultralytics.com/modes/train/)
- [Google Colab - Guía oficial](https://colab.research.google.com/notebooks/intro.ipynb)
- [Flickr Logos 27 Dataset](http://image.ntua.gr/iva/datasets/flickr_logos/)
