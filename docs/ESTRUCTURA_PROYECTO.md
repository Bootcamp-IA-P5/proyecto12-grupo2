# 📁 KUMO VISION - Estructura del Proyecto

```
proyecto12-grupo2/
│
├── 📄 README.md                    # Documentación principal del proyecto
├── 📄 requirements.txt             # Dependencias Python
├── 📄 docker-compose.yml           # Orquestación de servicios
├── 📄 Dockerfile.backend           # Imagen Docker del backend
├── 📄 .env.example                 # Plantilla de variables de entorno
├── 📄 .gitignore                   # Archivos ignorados por Git
│
├── 📂 docs/                        # 📚 DOCUMENTACIÓN
│   ├── README.md                   # Índice de documentación
│   ├── PRESENTACION_FINAL.md       # 🎤 Guía de presentación
│   ├── ACTUALIZACION_FINAL.md      # ⭐ Documentación técnica completa
│   ├── QUICKSTART.md               # Guía de inicio rápido
│   ├── SOLUCION_IMPLEMENTADA.md    # Arquitectura y decisiones
│   ├── RESUMEN_EJECUTIVO.md        # Resumen ejecutivo
│   ├── FRONTEND_ACTUALIZADO.md     # Documentación del frontend
│   ├── CHANGELOG.md                # Historial de cambios
│   ├── CAMBIOS_REALIZADOS.md       # Cambios detallados
│   ├── RESUMEN_FINAL.md            # Resumen final
│   ├── CLEANUP_SUMMARY.md          # Limpieza y optimización
│   ├── CHECKLIST_VERIFICACION.md   # Lista de verificación
│   ├── CONTRIBUTING.md             # Guía de contribución
│   └── COMMIT_GUIDE.md             # Convenciones de commits
│
├── 📂 frontend/                    # 🎨 FRONTEND - React + Vite
│   ├── 📄 package.json             # Dependencias Node.js
│   ├── 📄 vite.config.js           # Configuración Vite
│   ├── 📄 tailwind.config.js       # Configuración Tailwind CSS
│   ├── 📄 Dockerfile               # Imagen Docker frontend
│   ├── 📄 README.md                # Docs específica del frontend
│   │
│   ├── 📂 public/                  # Archivos estáticos
│   │   └── Gemini_Generated_Image_9t5mla9t5mla9t5m.png  # Logo KUMO
│   │
│   └── 📂 src/                     # Código fuente React
│       ├── main.jsx                # Entry point
│       ├── App.jsx                 # Componente principal
│       ├── App.css                 # Estilos principales
│       ├── index.css               # Estilos globales y variables
│       │
│       ├── 📂 components/          # Componentes React
│       │   ├── VideoAnalyzer.jsx   # Análisis de videos
│       │   ├── ImageAnalyzer.jsx   # Análisis de imágenes
│       │   ├── ResultsView.jsx     # Vista de resultados
│       │   ├── ModelInfo.jsx       # Información del modelo
│       │   └── SavedAnalyses.jsx   # Análisis guardados
│       │
│       └── 📂 assets/              # Assets del proyecto
│
├── 📂 src/                         # 🔧 BACKEND - FastAPI
│   ├── 📄 __init__.py
│   ├── 📄 data_augmentation.py     # Data augmentation (opcional)
│   ├── 📄 real_time_test.py        # Tests de tiempo real
│   │
│   └── 📂 demo/                    # Aplicación principal
│       ├── 📄 __init__.py
│       ├── 📄 settings.py          # Configuración centralizada
│       ├── 📄 README.md            # Docs del demo
│       │
│       ├── 📂 backend/             # ⚙️ API FastAPI
│       │   ├── __init__.py
│       │   ├── main.py             # 🌟 API endpoints principal
│       │   ├── model_worker.py     # YOLO detection (BrandInspector)
│       │   ├── database_manager.py # PostgreSQL manager
│       │   └── models.py           # SQLAlchemy models (Video, Detection)
│       │
│       ├── 📂 common/              # Utilidades comunes
│       │   ├── __init__.py
│       │   ├── logger.py           # Sistema de logging
│       │   └── log_setup.py        # Configuración de logs
│       │
│       ├── 📂 frontend/            # Streamlit (alternativo, no usado)
│       │   ├── __init__.py
│       │   └── app.py
│       │
│       └── 📂 log/                 # Archivos de log
│
├── 📂 models/                      # 🤖 MODELOS YOLO
│   ├── 📄 __init__.py
│   └── 📂 models_org/
│       ├── results.csv             # Resultados de entrenamiento
│       └── 📂 weights/
│           ├── best.pt             # 🏆 Modelo entrenado (mejor)
│           └── last.pt             # Último checkpoint
│
├── 📂 notebooks/                   # 📓 JUPYTER NOTEBOOKS
│   ├── 📄 __init__.py
│   ├── flickr_logos_mgg.ipynb      # Notebook de entrenamiento
│   └── flickr_logos_org.ipynb      # Notebook original
│
├── 📂 data/                        # 📊 DATOS
│   ├── 📄 __init__.py
│   ├── 📂 augmented_results/       # Resultados de augmentación
│   └── 📂 test_samples/            # Muestras de prueba
│       └── test_image.jfif
│
├── 📂 log/                         # 📝 LOGS DEL SISTEMA
│   └── kumo.log
│
├── 📂 .devcontainer/               # Dev Container config
│   └── devcontainer.json
│
├── 📂 .github/                     # GitHub workflows
│   └── workflows/
│
└── 📂 .git/                        # Control de versiones Git
```

---

## 🗂️ Descripción de Carpetas Principales

### `/docs/` - Documentación
Toda la documentación del proyecto:
- Técnica (API, arquitectura)
- Usuario (quickstart, guías)
- Desarrollo (contributing, commits)
- Presentación (slides, demo script)

### `/frontend/` - Aplicación Web React
Interfaz de usuario moderna:
- **5 componentes**: VideoAnalyzer, ImageAnalyzer, ResultsView, ModelInfo, SavedAnalyses
- **Tailwind CSS**: Design system con paleta azul KUMO
- **Recharts**: Gráficos interactivos
- **Vite**: Build tool ultra rápido

### `/src/demo/backend/` - API FastAPI
Backend con YOLO:
- **main.py**: 7 endpoints REST
- **model_worker.py**: BrandInspector (YOLO wrapper)
- **database_manager.py**: PostgreSQL ORM
- **models.py**: Schema de base de datos

### `/models/` - Modelos Entrenados
- **best.pt**: Modelo YOLOv8 entrenado en Flickr Logos
- Pesos persistentes, no se regeneran

### `/notebooks/` - Experimentación
Jupyter notebooks para:
- Entrenamiento del modelo
- Data augmentation
- Análisis exploratorio

---

## 📦 Archivos de Configuración

| Archivo | Propósito |
|---------|-----------|
| `docker-compose.yml` | Orquestación de backend, frontend, db |
| `Dockerfile.backend` | Imagen Python con FastAPI + YOLO |
| `frontend/Dockerfile` | Imagen Node.js con Vite |
| `requirements.txt` | Dependencias Python |
| `frontend/package.json` | Dependencias Node.js |
| `.env.example` | Plantilla de variables de entorno |
| `vite.config.js` | Config de Vite (HMR, proxy) |
| `tailwind.config.js` | Colores y extensiones Tailwind |

---

## 🚀 Archivos de Entrada

### Para Inicio Rápido
```bash
# Leer primero:
README.md              # Visión general
docs/QUICKSTART.md     # Setup en 5 minutos

# Ejecutar:
docker-compose up      # Levantar todo
```

### Para Desarrollo
```bash
# Entorno:
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Frontend:
cd frontend
npm install
npm run dev
```

---

## 🔗 Flujo de Datos

```
Usuario
  │
  ├──▶ frontend/src/App.jsx
  │      ├──▶ VideoAnalyzer.jsx ────┐
  │      ├──▶ ImageAnalyzer.jsx ────┤
  │      └──▶ SavedAnalyses.jsx ────┤
  │                                  │
  │                                  ▼
  └────────────────────────▶ src/demo/backend/main.py
                                     │
                    ┌────────────────┼────────────────┐
                    ▼                ▼                ▼
            model_worker.py   database_manager.py  models.py
                 (YOLO)          (PostgreSQL)      (Schema)
                    │                │
                    ▼                ▼
               models/weights/   PostgreSQL DB
                  best.pt        (Docker container)
```

---

## 📝 Notas Importantes

### Archivos Grandes
- `models/models_org/weights/best.pt` (~50-150 MB)
- Considerar Git LFS si commiteas modelos

### Archivos Generados (no commitear)
- `/__pycache__/`
- `/node_modules/`
- `/.venv/`
- `/dist/`
- `/log/*.log`
- `/data/augmented_results/*`

### Archivos Esenciales (siempre commitear)
- `README.md`
- `requirements.txt`
- `docker-compose.yml`
- `src/demo/backend/*.py`
- `frontend/src/**/*.jsx`
- `docs/*.md`

---

## 🎯 Archivos por Caso de Uso

### "Quiero entender el proyecto"
1. `README.md`
2. `docs/RESUMEN_EJECUTIVO.md`
3. `docs/ACTUALIZACION_FINAL.md`

### "Quiero ejecutarlo"
1. `README.md` → sección "Inicio Rápido"
2. `docker-compose up`

### "Quiero desarrollar"
1. `docs/QUICKSTART.md`
2. `docs/CONTRIBUTING.md`
3. `src/demo/backend/main.py`

### "Quiero presentarlo"
1. `docs/PRESENTACION_FINAL.md`
2. Slides (crear desde PRESENTACION_FINAL.md)
3. Demo: http://localhost:5173

---

**Última actualización**: 12 Febrero 2026  
**Mantenido por**: Grupo 2 - Bootcamp IA
