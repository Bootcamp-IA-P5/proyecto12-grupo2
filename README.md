# Proyecto 12 - KUMO VISION (Grupo 2)

Sistema completo de análisis de exposición de marcas en videos e imágenes usando YOLOv8, con frontend React y backend FastAPI + PostgreSQL.

---

## 📋 Descripción

KUMO VISION es un sistema de análisis que detecta y cuantifica la exposición de marcas en tiempo real. Incluye:

- **Frontend**: React 19 + Vite + Tailwind CSS con análisis en tiempo real y UI profesional
- **Backend**: FastAPI con streaming NDJSON para progreso en vivo
- **Base de Datos**: PostgreSQL para almacenar análisis históricos
- **IA**: YOLOv8 entrenado en dataset de logos Flickr

---

## 🚀 Características

- ✅ **Análisis de videos** (YouTube URLs + archivos locales)
- ✅ **Análisis de imágenes estáticas** (JPG, PNG, etc.)
- ✅ Progreso en tiempo real con streaming NDJSON
- ✅ Visualización con gráficos interactivos (Recharts PieChart)
- ✅ Base de datos PostgreSQL para análisis guardados
- ✅ UI moderna y responsive con diseño KUMO VISION
- ✅ Backend FastAPI con CORS configurado
- ✅ Contenedorización con Docker Compose
- ✅ Métricas detalladas: exposición por marca, visibilidad, detecciones
- ✅ **Control de guardado**: Usuario decide qué análisis conservar

---

## ⚡ Inicio Rápido con Docker

### Método Recomendado: Docker Compose

```bash
# Desde la raíz del proyecto
docker-compose up --build
```

Luego abrir: **http://localhost:5173**

### URLs de Acceso

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:9000
- **API Documentation**: http://localhost:9000/docs
- **PostgreSQL**: localhost:5432 (usuario: postgres, pass: postgres)

---

## 📚 Documentación

Toda la documentación técnica está organizada en la carpeta [`docs/`](docs/):

### 📖 Documentos Clave

- **[📚 Índice de Documentación](docs/README.md)** - Navegación completa
- **[🎤 Guía de Presentación](docs/PRESENTACION_FINAL.md)** - Script y slides para demo
- **[⭐ Documentación Técnica](docs/ACTUALIZACION_FINAL.md)** - TODO sobre el sistema
- **[🚀 Quickstart](docs/QUICKSTART.md)** - Setup en 5 minutos
- **[📁 Estructura del Proyecto](docs/ESTRUCTURA_PROYECTO.md)** - Organización de archivos

### Por Audiencia

| Audiencia | Documento Recomendado |
|-----------|----------------------|
| **Desarrolladores** | [ACTUALIZACION_FINAL.md](docs/ACTUALIZACION_FINAL.md) |
| **Product Managers** | [RESUMEN_EJECUTIVO.md](docs/RESUMEN_EJECUTIVO.md) |
| **Presentadores** | [PRESENTACION_FINAL.md](docs/PRESENTACION_FINAL.md) |
| **Nuevos Usuarios** | [QUICKSTART.md](docs/QUICKSTART.md) |

---

## 📁 Estructura del Proyecto

```
proyecto12-grupo2/
├── frontend/                # Frontend React
│   ├── src/
│   │   ├── components/     # 5 componentes funcionales
│   │   │   ├── VideoAnalyzer.jsx    # Análisis de videos
│   │   │   ├── ImageAnalyzer.jsx    # ⭐ Análisis de imágenes
│   │   │   ├── ResultsView.jsx      # Vista de resultados
│   │   │   ├── ModelInfo.jsx        # Info del modelo
│   │   │   └── SavedAnalyses.jsx    # Histórico
│   │   ├── App.jsx         # Componente principal con tabs
│   │   ├── App.css         # Estilos KUMO VISION
│   │   └── main.jsx
│   ├── public/
│   │   └── Gemini_Generated_Image_9t5mla9t5m.png  # Logo KUMO
│   ├── Dockerfile
│   └── package.json
├── src/demo/               # Backend FastAPI
│   ├── backend/
│   │   ├── main.py         # API FastAPI (puerto 9000)
│   │   ├── model_worker.py # YOLO detection (video + imagen)
│   │   ├── database_manager.py  # PostgreSQL manager
│   │   └── models.py       # SQLAlchemy models
│   ├── common/             # Logging utilities
│   └── settings.py         # Configuración centralizada
├── models/                 # Modelos YOLO
│   └── models_org/
│       └── weights/
│           └── best.pt     # Modelo entrenado
├── docker-compose.yml      # Orquestación de servicios
├── Dockerfile.backend      # Imagen del backend
└── requirements.txt        # Dependencias Python

## 🔌 API Endpoints

### Análisis

- `POST /analyze/` - Analizar video local (upload)
- `POST /analyze-stream/` - Analizar video de YouTube (URL)
- `POST /analyze-image/` - ⭐ **NUEVO**: Analizar imagen estática

### Resultados

- `GET /results/{video_id}` - Obtener resultados guardados
- `DELETE /results/{video_id}` - Eliminar análisis
- `POST /save-analysis/?video_id=xxx` - Guardar análisis en DB

### Información

- `GET /model-info/` - Info del modelo YOLO (marcas detectables)

### Formato de Respuesta (Videos e Imágenes)

```json
{
  "status": "success",
  "video_id": "uuid-or-image-id",
  "title": "nombre_archivo",
  "total_duration": 120.5,
  "total_exposure_time": 45.2,
  "visibility_percentage": 37.5,
  "brands": {
    "Nike": {
      "detections": 15,
      "exposure_time": 25.3,
      "visibility": 20.8,
      "sample_images": []
    },
    "Adidas": {
      "detections": 8,
      "exposure_time": 19.9,
      "visibility": 16.5,
      "sample_images": []
    }
  }
}
```
│   └── models_org/weights/
│       └── best.pt         # YOLO weights
├── docs/                   # Documentación técnica
│   ├── FRONTEND_ACTUALIZADO.md
│   ├── CHECKLIST_VERIFICACION.md
│   ├── RESUMEN_EJECUTIVO.md
│   └── SOLUCION_IMPLEMENTADA.md
├── .env                    # Configuración ÚNICA
├── start-full.sh          # Script de inicio
└── docker-compose-demo.yml
```

## 🔧 Configuración

### Variables de Entorno (.env)

**El proyecto usa UN SOLO archivo .env en la raíz:**

```env
# PostgreSQL
POSTGRES_DB=brandtracker
POSTGRES_USER=admin
POSTGRES_PASSWORD=password123
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Backend FastAPI (puerto 8001)
BACKEND_URL=http://localhost:8001

# Frontend
VITE_API_URL=http://localhost:8001
NODE_ENV=development
```

**Nota:** El frontend usa un symlink a este archivo. NO crear .env adicionales en /frontend.

## 🛠️ Requisitos

- Docker & Docker Compose
- Node.js 20+ (para desarrollo local)
- Python 3.13 (dentro del contenedor)

## 🐳 Instalación y Ejecución

### Con Docker Compose (Recomendado)

```bash
# Clonar el repositorio
git clone <repo-url>
cd proyecto12-grupo2

# Ejecutar todos los servicios
docker-compose -f docker-compose-demo.yml up --build
```

**Servicios disponibles:**
- 🎨 Frontend React: `http://localhost:5173`
- 📊 Streamlit Demo: `http://localhost:8501`

### Desarrollo Local

#### Backend
```bash
pip install -r requirements.txt
python run_api.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## � Documentación

### Documentos Principales
- **[QUICKSTART.md](QUICKSTART.md)** - Guía rápida de inicio
- **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía de contribución
- **[COMMIT_GUIDE.md](COMMIT_GUIDE.md)** - Guía de commits

### Documentación Técnica Detallada
- **[docs/FRONTEND_ACTUALIZADO.md](docs/FRONTEND_ACTUALIZADO.md)** - Guía completa del frontend
- **[docs/CHECKLIST_VERIFICACION.md](docs/CHECKLIST_VERIFICACION.md)** - Checklist de verificación
- **[docs/RESUMEN_EJECUTIVO.md](docs/RESUMEN_EJECUTIVO.md)** - Resumen ejecutivo
- **[docs/SOLUCION_IMPLEMENTADA.md](docs/SOLUCION_IMPLEMENTADA.md)** - Detalles técnicos de solución

### Cambios Recientes
- **[CAMBIOS_REALIZADOS.md](CAMBIOS_REALIZADOS.md)** - Resumen de cambios recientes
- **[CLEANUP_SUMMARY.md](CLEANUP_SUMMARY.md)** - Detalles de limpieza del proyecto

## 🎯 Arquitectura

```
┌─────────────────┐
│ React Frontend  │  Puerto 5173
│   (Vite + UI)   │
└────────┬────────┘
         │ HTTP + NDJSON Streaming
         ↓
┌─────────────────┐
│  FastAPI Backend│  Puerto 8001
│ (+ CORS)        │
└────────┬────────┘
         │ SQLAlchemy
         ↓
┌─────────────────┐
│   PostgreSQL    │  Puerto 5432
│   brandtracker  │
└─────────────────┘
         ↑
         │ Model
    ┌────┴─────┐
    │   YOLO   │
    │ Detection│
    └──────────┘
```

## 🐛 Troubleshooting

### Pantalla negra en el frontend
Verificar que el backend esté corriendo en puerto 8001:
```bash
curl http://localhost:8001/model-info/
## 🐛 Troubleshooting

### Backend no inicia
```bash
docker-compose logs backend
# Verificar logs de error
# Común: modelo YOLO no cargado o puertos ocupados
```

### Frontend no conecta al backend
```bash
# Verificar VITE_API_URL
docker-compose exec frontend env | grep VITE
# Debe ser http://localhost:9000
```

### Database no conecta
```bash
# Verificar que PostgreSQL esté running
docker-compose ps
# Recrear volumen si está corrupto
docker-compose down -v
docker-compose up --build
```

### Resultados muestran 0.0s
- **Causa**: Modelo no detectó marcas (umbral conf=0.25)
- **Solución**: Usar video/imagen con marcas visibles
- **Debug**: `docker-compose logs backend`

**Ver más en**: [docs/ACTUALIZACION_FINAL.md](docs/ACTUALIZACION_FINAL.md#troubleshooting)

---

## 📦 Stack Tecnológico Completo

### Backend
- **FastAPI** - Framework API REST moderno
- **YOLOv8** (Ultralytics) - Detección de objetos
- **PostgreSQL** - Base de datos relacional
- **SQLAlchemy** - ORM Python
- **yt-dlp** - Descarga de videos YouTube
- **OpenCV** - Procesamiento de imágenes/videos
- **Python 3.11** - Lenguaje base

### Frontend
- **React 19** - Framework UI moderno
- **Vite** - Build tool ultra rápido
- **Tailwind CSS** - Framework de estilos
- **Recharts** - Gráficos interactivos
- **NDJSON Streaming** - Progreso en tiempo real

### DevOps
- **Docker** - Contenedorización
- **Docker Compose** - Orquestación multi-contenedor
- **GitHub** - Versionado y colaboración
- **Dev Containers** - Entorno de desarrollo consistente

---

## 👥 Equipo y Contacto

**Grupo 2 - Bootcamp IA Uniminuto**  
Proyecto 12 - Computer Vision  
Febrero 2026

### Enlaces
- **Repositorio**: [Bootcamp-IA-P5/proyecto12-grupo2](https://github.com/Bootcamp-IA-P5/proyecto12-grupo2)
- **Documentación**: [docs/](docs/)
- **Issues**: GitHub Issues

---

## 📌 Estado del Proyecto

### ✅ Completado
- [x] Análisis de videos (local + YouTube)
- [x] Análisis de imágenes estáticas
- [x] Frontend React con UI profesional
- [x] Backend FastAPI con 7 endpoints
- [x] Base de datos PostgreSQL
- [x] Streaming de progreso en tiempo real
- [x] Visualización con gráficos
- [x] Sistema de guardado controlado
- [x] Dockerización completa
- [x] Documentación exhaustiva

### 🔮 Mejoras Futuras
- [ ] Captura de frames con detecciones
- [ ] Aceleración GPU (CUDA)
- [ ] Batch processing
- [ ] Exportar reportes PDF/Excel
- [ ] Dashboard empresarial

**Ver roadmap completo**: [docs/ACTUALIZACION_FINAL.md](docs/ACTUALIZACION_FINAL.md#-mejoras-futuras-sugeridas)

---

## 📄 Licencia

Este proyecto fue desarrollado con fines educativos como parte del Bootcamp de IA de Uniminuto.

---

## 🙏 Agradecimientos

- **Uniminuto** - Bootcamp IA
- **Ultralytics** - Framework YOLOv8
- **FastAPI** - Framework backend
- **React Team** - Framework frontend

---

**¿Preguntas?** Consulta la [documentación completa](docs/) o abre un issue en GitHub.

**¡Gracias por usar KUMO VISION!** 🚀
- [ ] Testing integral
- [ ] Documentación API (Swagger/OpenAPI)


## 📸 Galería de Aumento de Datos (Data Augmentation)

Para mejorar la robustez de nuestro modelo **KUMO VISION**, hemos implementado un pipeline de procesamiento de imágenes. Un modelo de IA es tan bueno como los datos con los que se entrena; por ello, mediante estas técnicas, ayudamos a que la red neuronal generalice mejor ante situaciones del mundo real.

A continuación, se presentan los resultados de las transformaciones aplicadas a nuestro dataset:

| Imagen Original | Volteo (Flip) | Ajuste de Color (Jitter) | Recorte Aleatorio (Crop) |
| :---: | :---: | :---: | :---: |
| ![Original](data/test_samples/test_image.jfif) | ![Flip](data/augmented_results/sample_flip.jpg) | ![Jitter](data/augmented_results/sample_jitter.jpg) | ![Crop](data/augmented_results/sample_crop.jpg) |

### 🛠️ ¿Por qué usamos estas técnicas?
1. **Volteo Horizontal:** Permite que el modelo reconozca los objetos sin importar su orientación lateral.
2. **Ajuste de Color (Jitter):** Simula diferentes condiciones de iluminación y sensores de cámara, haciendo que la detección sea fiable tanto en días soleados como en interiores oscuros.
3. **Recorte Aleatorio (Crop):** Ayuda al modelo a enfocarse en las características del objeto incluso si este no aparece centrado o se encuentra a diferentes distancias.

> *Nota: Estas transformaciones se generan dinámicamente para enriquecer el entrenamiento sin necesidad de capturar manualmente miles de fotos nuevas.*

## 📂 Ramas

- `development` - Rama principal de desarrollo
- `feature-initial-react-frontend` - Setup frontend React 
- `feat-data-techniques-for-model-robustization` 


## 📄 Licencia

Proyecto educativo - Bootcamp IA 
