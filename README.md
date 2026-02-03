# Proyecto 12 - Detección de Logos (Grupo 2)

Sistema de detección de logos con interfaz web usando React y backend con Streamlit/FastAPI.

## 📋 Descripción

Este proyecto implementa un sistema de detección y reconocimiento de logos en imágenes utilizando Computer Vision con modelos de Deep Learning (YOLOv8). Incluye:

- **Frontend**: Interfaz React moderna con Vite y Tailwind CSS
- **Backend**: API Streamlit para procesamiento de imágenes (En desarrollo)
- **Modelos**: YOLOv8 entrenado en dataset de logos Flickr

## 🚀 Características

- ✅ Interfaz web responsiva (React + Tailwind)
- ✅ Contenedorización con Docker Compose
- ✅ Soporte para ambiente de desarrollo (Dev Container)
- 🔄 Backend API en desarrollo (conexión a modelos)
- 📊 Modelos pre-entrenados en `/models/models_org/weights/`

## 📁 Estructura del Proyecto

```
proyecto12-grupo2/
├── frontend/              # Aplicación React con Vite
│   ├── src/
│   │   ├── components/   # Componentes React reutilizables
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── src/                  # Backend Python
│   ├── api.py           # API principal (pendiente)
│   ├── api_simple.py    # API simple
│   └── demo/            # Aplicación Streamlit
├── models/              # Modelos pre-entrenados
│   └── models_org/
│       └── weights/
│           ├── best.pt
│           └── last.pt
├── notebooks/           # Jupyter notebooks
└── docker-compose-demo.yml  # Orquestación de servicios
```

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

## 📝 Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz:

```env
# Backend
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0

# Frontend (si es necesario)
VITE_API_URL=http://localhost:8000
```

## 🔌 Integración Backend-Frontend

> ⚠️ **Estado Actual**: El backend está en desarrollo. El modelo aún no está completamente integrado.

Para conectar el frontend con la API:

1. Actualizar `VITE_API_URL` en `.env`
2. Implementar endpoints en backend (pendiente)
3. Configurar CORS en FastAPI/Streamlit

## 🧪 Testing

```bash
# Test API
python test_api.py

# Lint Frontend
cd frontend && npm run lint
```

## 📦 Stack Tecnológico

### Frontend
- **React 19** - Librería UI
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **ESLint** - Linting

### Backend
- **Streamlit** - Interface para demos
- **FastAPI** - API REST (planeado)
- **YOLOv8** - Detección de objetos
- **PyTorch** - Framework ML

## 👥 Equipo

- Grupo 2 - Bootcamp IA

## 📌 Estado del Proyecto

- [x] Setup inicial con React + Vite
- [x] Configuración Docker & Docker Compose
- [x] Integración Dev Container
- [ ] Implementación completa de API backend
- [ ] Conexión modelos con API
- [ ] Testing integral
- [ ] Documentación API (Swagger/OpenAPI)

## 📂 Ramas

- `development` - Rama principal de desarrollo
- `feature-initial-react-frontend` - Setup frontend React (actual)

## 📄 Licencia

Proyecto educativo - Bootcamp IA 
