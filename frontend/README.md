# BrandTracker AI - Frontend

Frontend React moderno para el sistema de análisis de exposición de marcas en videos.

## 🎯 Características

- ✅ Análisis de videos desde YouTube URLs
- ✅ Análisis de videos subidos localmente (MP4, AVI, MOV, MKV)
- ✅ Streaming de progreso en tiempo real (NDJSON)
- ✅ Visualización de resultados con gráficos interactivos
- ✅ Integración con base de datos PostgreSQL
- ✅ Gestión de análisis guardados
- ✅ UI moderna con Tailwind CSS

## 🏗️ Arquitectura

```
Frontend (React + Vite)
  ↓ HTTP/NDJSON
Backend FastAPI (Puerto 8001)
  ↓ SQLAlchemy
PostgreSQL Database
  ↓ YOLO Model
Brand Detection
```

## 📦 Tecnologías

- **React 19** - Framework UI
- **Vite** - Build tool y dev server
- **Tailwind CSS** - Estilos
- **Recharts** - Gráficos interactivos
- **Fetch API** - HTTP requests y streaming

## 🚀 Inicio Rápido

### Opción 1: Script automático (recomendado)

Desde la raíz del proyecto:

```bash
./start-full.sh
```

### Opción 2: Inicio manual

#### 1. Backend (Terminal 1)

```bash
# Desde la raíz del proyecto
source .venv/bin/activate
cd src/demo
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

#### 2. Frontend (Terminal 2)

```bash
cd frontend
npm install  # Solo la primera vez
npm run dev
```

## 🌍 URLs

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8001
- **API Docs**: http://localhost:8001/docs

## 📁 Estructura

```
src/
├── App.jsx                     # Componente principal
├── components/
│   ├── VideoAnalyzer.jsx       # Análisis de videos
│   ├── ResultsView.jsx         # Visualización de resultados
│   ├── ModelInfo.jsx           # Info del modelo
│   └── SavedAnalyses.jsx       # Historial
├── App.css                     # Estilos
└── index.css                   # Tailwind base
```

## 🔧 Configuración

Crear archivo `.env`:

```env
VITE_API_URL=http://localhost:8001
NODE_ENV=development
```

## 📊 Flujo de Análisis

1. Usuario selecciona video (YouTube URL o archivo)
2. Frontend envía request a backend
3. Backend procesa con YOLO y envía actualizaciones NDJSON
4. Frontend actualiza UI en tiempo real
5. Resultados se guardan en PostgreSQL
6. Frontend muestra gráficos y métricas

## 🐛 Troubleshooting

### Pantalla negra

Verificar que el backend esté corriendo en puerto 8001 y que CORS esté configurado.

### Error de CORS

Verificar que el backend tenga CORSMiddleware configurado.

### Backend no responde

Verificar PostgreSQL y el modelo YOLO en `models/models_org/weights/best.pt`.

## 👥 Equipo

Grupo 2 - Bootcamp IA P5
