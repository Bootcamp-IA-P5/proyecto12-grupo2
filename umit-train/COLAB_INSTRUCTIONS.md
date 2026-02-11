# 🚀 Entrenar en Google Colab - Guía Rápida

## ✅ Preparación (5 minutos)

### 1. Descargar el Dataset

**Flickr Logos 27 Dataset:**
- Link: http://image.ntua.gr/iva/datasets/flickr_logos/
- O usar este enlace directo: [Descargar ZIP](https://www.dropbox.com/s/0b6zcvdxo9w2z7h/flickr_logos_27_dataset.zip?dl=1)

### 2. Subir a Google Drive

**Archivos necesarios:**
1. `flickr_logos_27_dataset.zip` (el dataset descargado)
2. `data.yaml` (ya creado en este directorio)

**Pasos:**
1. Ve a [Google Drive](https://drive.google.com)
2. Sube ambos archivos a la **raíz** de "Mi unidad"

**Estructura en Drive:**
```
Mi unidad/
├── flickr_logos_27_dataset.zip    ← Dataset
└── data.yaml                       ← Configuración
```

---

## 🎯 Entrenar en Colab (30 minutos)

### Paso 1: Abrir Notebook en Colab

**Opción A: Subir manualmente**
1. Ve a https://colab.research.google.com
2. Click **File → Upload notebook**
3. Sube: `train_yolo_colab.ipynb` (de este directorio)

**Opción B: Desde GitHub** ⭐ Recomendado
1. Ve a https://colab.research.google.com
2. Click **File → Open notebook → GitHub**
3. Pega: `https://github.com/Bootcamp-IA-P5/proyecto12-grupo2`
4. Selecciona la rama: `14-make-model-tests-with-more-photos`
5. Selecciona: `umit-train/train_yolo_colab.ipynb`

### Paso 2: Activar GPU (IMPORTANTE ⚡)

1. En Colab: **Runtime → Change runtime type**
2. **Hardware accelerator**: T4 GPU
3. Click **Save**

### Paso 3: Ejecutar Celdas

Ejecuta en orden (Shift + Enter en cada celda):

```
1️⃣ Montar Google Drive
2️⃣ Instalar Ultralytics  
3️⃣ Verificar GPU
4️⃣ Descomprimir dataset
5️⃣ ENTRENAR (espera 20-30 min) ☕
6️⃣ Ver resultados
7️⃣ Validar modelo
```

### Paso 4: Descargar el Modelo

Al finalizar, ejecuta esta celda en Colab:

```python
# Copiar a Drive
!cp /content/runs/detect/logos_flickr_dataset/weights/best.pt /content/drive/MyDrive/best.pt

# O descargar directamente
from google.colab import files
files.download('/content/runs/detect/logos_flickr_dataset/weights/best.pt')
```

---

## 📥 Después del Entrenamiento

### 1. Colocar el modelo en el proyecto

```bash
# Crear directorio
mkdir -p models/models_org/weights

# Copiar desde Descargas
cp ~/Downloads/best.pt models/models_org/weights/best.pt
```

### 2. Ejecutar evaluación

```bash
# Activar entorno
source .venv/bin/activate

# Evaluar modelo
python tests/model_evaluation/evaluate_model.py
```

---

## 🎯 Checklist

**Antes de entrenar:**
- [ ] Dataset descargado
- [ ] `flickr_logos_27_dataset.zip` subido a Google Drive
- [ ] `data.yaml` subido a Google Drive
- [ ] Notebook abierto en Colab
- [ ] **GPU T4 activada** (Runtime → Change runtime type)

**Durante el entrenamiento:**
- [ ] Drive montado correctamente
- [ ] GPU detectada (nvidia-smi muestra T4)
- [ ] Dataset descomprimido sin errores
- [ ] Entrenamiento iniciado (verás el progreso)

**Después del entrenamiento:**
- [ ] `best.pt` descargado
- [ ] Modelo copiado a `models/models_org/weights/best.pt`
- [ ] Evaluación ejecutada correctamente

---

## 📊 Métricas Esperadas

Después de 50 epochs:
- **mAP50**: 0.70 - 0.85
- **Precisión**: 0.75 - 0.90
- **Tiempo**: 20-30 minutos en T4 GPU

---

## ⚠️ Problemas Comunes

**GPU no detectada**
```
Runtime → Change runtime type → T4 GPU → Save
Runtime → Restart runtime
```

**Dataset no encontrado**
```
Verifica que flickr_logos_27_dataset.zip esté en la raíz de Drive
(No en carpetas como "Colab Notebooks")
```

**Error en data.yaml**
```
Sube data.yaml a la raíz de Google Drive
```

**Se desconecta Colab**
```
Colab gratis tiene límite de 12 horas
Abre una pestaña para mantener la sesión activa
```

---

## 🔗 Enlaces Útiles

- [Google Colab](https://colab.research.google.com)
- [Google Drive](https://drive.google.com)
- [Dataset Flickr Logos 27](http://image.ntua.gr/iva/datasets/flickr_logos/)
- [Documentación YOLO](https://docs.ultralytics.com)

---

¡Listo! Ahora solo sube los archivos a Drive y ejecuta el notebook en Colab 🚀
