# 🛡️ BrandTracker AI - Detección de Logos en Videos

Sistema de detección de logos/marcas en imágenes y videos usando YOLOv11, desarrollado como proyecto del Bootcamp de IA.

## 🎯 Objetivo del Proyecto

Crear un modelo de detección de marcas en videos para analizar el tiempo de exposición de logos y generar informes automáticos sobre la presencia de marcas en contenido multimedia.

---

## ✅ Estado Actual del Proyecto

### 🏆 Nivel Completado: **Medio-Avanzado**

- ✅ **Modelo entrenado** con YOLOv11 (50 epochs)
- ✅ **Dataset**: Flickr Logos 27 (27 marcas)
- ✅ **Detección en imágenes** funcionando
- ✅ **Detección en videos** funcionando
- ✅ **Demo con Streamlit** (por Oscar)
- ✅ **Docker** configurado
- ✅ **Evaluación exhaustiva** completada

### 📊 Resultados de Pruebas

**Prueba con Video (63s):**
- 12 marcas detectadas
- Coca-Cola: 70% confianza ✅
- Ford: 78% confianza ✅
- Nike: 52% confianza
- McDonald's: 53% confianza

**Prueba con Imágenes (21 total):**
- Tasa de detección: 25-31%
- Mejor resultado: Pepsi 94%

---

## 🚀 Quick Start

### Requisitos Previos
```bash
Python 3.11+
pip
virtualenv (opcional pero recomendado)
```

### Instalación

```bash
# Clonar repositorio
git clone https://github.com/Bootcamp-IA-P5/proyecto12-grupo2.git
cd proyecto12-grupo2

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
```

### Usar la Demo (Streamlit)

```bash
# Opción 1: Docker (Recomendado)
docker compose -f docker-compose-demo.yml up -d

# Abrir en navegador
open http://localhost:8501

# Opción 2: Local
streamlit run src/demo/app.py
```

### Evaluar el Modelo

```bash
# Evaluar con imágenes
python tests/model_evaluation/evaluate_model.py

# Probar con un video
python tests/test_video.py tests/test_videos/tu_video.mp4

# Jupyter Notebook interactivo
jupyter notebook tests/model_evaluation.ipynb
```

---

## 📁 Estructura del Proyecto

```
proyecto12-grupo2/
├── models/
│   └── models_org/weights/
│       └── best.pt              # Modelo YOLOv11 entrenado (5.2MB)
├── src/
│   └── demo/                    # Aplicación Streamlit
│       ├── app.py
│       ├── database.py
│       └── settings.py
├── tests/
│   ├── test_images/             # Imágenes de prueba
│   ├── test_videos/             # Videos de prueba
│   ├── results/                 # Resultados JSON
│   ├── test_logo_images.py      # Script de prueba imágenes
│   ├── test_video.py            # Script de análisis de video
│   └── model_evaluation.ipynb   # Notebook de evaluación
├── umit-train/
│   ├── train_yolo_colab.ipynb   # Notebook para entrenar en Colab
│   ├── data.yaml                # Configuración del dataset
│   └── COLAB_INSTRUCTIONS.md    # Guía de entrenamiento
├── docker-compose-demo.yml      # Configuración Docker
└── requirements.txt             # Dependencias Python
```

---

## 🎓 Marcas Detectables (27 total)

```
Adidas, Apple, BMW, Citroen, Coca Cola, DHL, Fedex, Ferrari, Ford,
Google, HP, Heineken, Intel, McDonalds, Mini, Nbc, Nike, Pepsi,
Porsche, Puma, Red Bull, Sprite, Starbucks, Texaco, Unicef,
Vodafone, Yahoo
```

---

## 🔧 Tecnologías Utilizadas

- **Python 3.11**
- **YOLOv11** (Ultralytics)
- **OpenCV** para procesamiento de video
- **Streamlit** para la interfaz web
- **PostgreSQL** para base de datos
- **Docker** para containerización
- **Google Colab** para entrenamiento con GPU

---

## 📚 Documentación

- [Guía de Entrenamiento en Colab](umit-train/COLAB_INSTRUCTIONS.md)
- [Resultados de Pruebas Detallados](tests/RESULTADOS.md)
- [README de Tests](tests/README.md)

---

## 👥 Equipo

**Bootcamp IA - Proyecto 12 - Grupo 2**
- Umit Gungor - Entrenamiento del modelo y evaluación
- Oscar Rodriguez - Demo Streamlit y Docker

---

## 📝 Licencia

Proyecto educativo - Bootcamp de IA

---

## 🔗 Enlaces Útiles

- [Documentación YOLO](https://docs.ultralytics.com)
- [Flickr Logos 27 Dataset](http://image.ntua.gr/iva/datasets/flickr_logos/)
- [Google Colab](https://colab.research.google.com)
