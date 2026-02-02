# Configuración de Ambiente

## Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true

# Frontend Configuration
VITE_API_URL=http://localhost:8501
VITE_APP_TITLE=Logo Detector

# Python/Backend
PYTHONUNBUFFERED=1
```

## Variables .env.local (Frontend)

Crear `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8501
VITE_APP_TITLE=Detección de Logos
```

## Descripción de Variables

| Variable | Descripción | Default |
|----------|-------------|---------|
| `STREAMLIT_SERVER_PORT` | Puerto del servidor Streamlit | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Dirección de binding para Streamlit | 0.0.0.0 |
| `VITE_API_URL` | URL de la API backend desde el frontend | http://localhost:8501 |
| `PYTHONUNBUFFERED` | Python sin buffer para logs en tiempo real | 1 |

## Ambiente de Desarrollo

Para desarrollo local (sin Docker):

```bash
# 1. Crear virtual environment
python -m venv .venv

# 2. Activar
# En Windows:
.venv\Scripts\activate
# En Linux/Mac:
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Setup frontend
cd frontend
npm install
```

## Seguridad

⚠️ **IMPORTANTE**: Nunca comitear archivos `.env` con valores secretos. Usar:
- `.env.example` con valores de ejemplo
- `.env.local` para desarrollo local
- Variables de entorno en producción

Ver `.gitignore` para archivos excluidos.
