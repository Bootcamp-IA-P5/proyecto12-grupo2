# Evaluación del Modelo - Guía de Uso

## ⚠️ Modelo no encontrado

Para ejecutar las pruebas de evaluación, primero necesitas:

### 1. Entrenar el modelo o descargar un modelo pre-entrenado

**Opción A: Entrenar tu propio modelo**

Si ya tienes el notebook `umit-train/train_yolo_colab.ipynb`, ejecútalo en Google Colab para entrenar el modelo. Al finalizar:

1. Descarga el modelo entrenado (`best.pt`)
2. Colócalo en: `models/models_org/weights/best.pt`

**Opción B: Usar un modelo YOLO pre-entrenado de prueba**

```bash
# Crear directorio
mkdir -p models/models_org/weights

# Descargar modelo YOLOv8 pre-entrenado (solo para pruebas iniciales)
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt -O models/models_org/weights/best.pt
```

### 2. Ejecutar evaluación

Una vez tengas el modelo:

```bash
# Asegúrate de estar en el entorno virtual
source .venv/bin/activate

# Ejecutar evaluación
python tests/model_evaluation/evaluate_model.py
```

### 3. Usar el Jupyter Notebook

```bash
# Iniciar Jupyter
jupyter notebook tests/model_evaluation.ipynb
```

## 📁 Estructura esperada

```
proyecto12-grupo2/
├── models/
│   └── models_org/
│       └── weights/
│           └── best.pt          ← Modelo entrenado necesario aquí
├── tests/
│   ├── test_images/             ← Imágenes descargadas ✅
│   ├── test_videos/             ← Añade videos aquí
│   ├── results/                 ← Resultados se guardarán aquí
│   ├── model_evaluation/
│   │   └── evaluate_model.py    ← Script de evaluación ✅
│   ├── download_test_data.py    ← Script ejecutado ✅
│   └── model_evaluation.ipynb   ← Notebook creado ✅
```

## 🎯 Próximos pasos

1. ✅ Descargadas 8 imágenes de prueba en `tests/test_images/`
2. ⚠️ **PENDIENTE:** Obtener modelo entrenado `best.pt`
3. ⏭️ Ejecutar evaluación con `python tests/model_evaluation/evaluate_model.py`
4. ⏭️ Revisar resultados en `tests/results/evaluation_results.json`

## 🔗 Recursos

- [Entrenar YOLOv8/v11](https://docs.ultralytics.com/modes/train/)
- [Modelos pre-entrenados YOLO](https://github.com/ultralytics/ultralytics)
- Tu notebook de entrenamiento: `umit-train/train_yolo_colab.ipynb`
