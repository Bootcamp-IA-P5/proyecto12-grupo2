# 🚀 Quick Start Guide

Guía rápida para empezar con el proyecto.

## Opción 1: Docker Compose (Recomendado ⭐)

```bash
# 1. Clonar repo
git clone <repo-url>
cd proyecto12-grupo2

# 2. Ejecutar servicios
docker-compose -f docker-compose-demo.yml up --build

# 3. Acceder a:
# - Frontend: http://localhost:5173
# - Streamlit: http://localhost:8501
```

**Ventajas:**
- ✅ Todo aislado en contenedores
- ✅ No requiere instalaciones locales
- ✅ Reproducible en cualquier máquina
- ✅ Mismo ambiente que producción

## Opción 2: Desarrollo Local Dividido

### Terminal 1 - Backend
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -r requirements.txt
python run_api.py
# Streamlit: http://localhost:8501
```

### Terminal 2 - Frontend
```bash
cd frontend
npm install
npm run dev
# React: http://localhost:5173
```

**Ventajas:**
- ✅ Hot reload en ambos lados
- ✅ Más rápido para desarrollo
- ✅ Debug más fácil

## Opción 3: Dev Container (VS Code)

```bash
# En VS Code:
1. Press Ctrl+Shift+P
2. Escribe: "Dev Containers: Reopen in Container"
3. Ejecuta: python run_api.py
```

**Ventajas:**
- ✅ Ambiente de desarrollo completo
- ✅ Todas las herramientas incluidas
- ✅ Consistente para todo el equipo

---

## 📝 Configuración Básica

### `.env` (Opcional)
```env
STREAMLIT_SERVER_PORT=8501
VITE_API_URL=http://localhost:8501
```

Ver `ENVIRONMENT.md` para todas las variables.

---

## 📁 Estructura Principal

```
proyecto12-grupo2/
├── frontend/          # React + Vite (Puerto 5173)
├── src/              # Backend Python
│   └── demo/        # Streamlit app (Puerto 8501)
├── models/          # YOLOv8 weights
└── notebooks/       # Jupyter notebooks
```

---

## 🛠️ Comandos Comunes

### Docker
```bash
# Iniciar con rebuild
docker-compose -f docker-compose-demo.yml up --build

# Parar servicios
docker-compose -f docker-compose-demo.yml down

# Ver logs
docker-compose -f docker-compose-demo.yml logs -f

# Solo frontend
docker-compose -f docker-compose-demo.yml up frontend
```

### Frontend
```bash
cd frontend

npm run dev      # Desarrollo (http://localhost:5173)
npm run build    # Producción
npm run lint     # Validar código
npm run preview  # Preview de build
```

### Backend
```bash
python run_api.py       # Iniciar Streamlit
python test_api.py      # Ejecutar tests
python run.sh           # Script alternativo
```

---

## ❓ Troubleshooting

### Puerto 5173 está ocupado
```bash
# Cambiar puerto en docker-compose-demo.yml:
ports:
  - "5174:5173"  # Usar 5174 en lugar de 5173
```

### node_modules error en Docker
```bash
# Solución: Ya agregamos .dockerignore
docker-compose -f docker-compose-demo.yml build --no-cache
```

### Python: ModuleNotFoundError
```bash
# Verificar venv activado
.venv\Scripts\activate

# Reinstalar dependencias
pip install -r requirements.txt
```

### Frontend no conecta a backend
- Verificar `VITE_API_URL` en `.env`
- Verificar que backend está en puerto 8501
- Revisar CORS configuration (próximo paso)

---

## 📚 Documentación Completa

- 📖 [README.md](README.md) - Overview del proyecto
- 📝 [CHANGELOG.md](CHANGELOG.md) - Historial de cambios
- 🤝 [CONTRIBUTING.md](CONTRIBUTING.md) - Cómo contribuir
- ⚙️ [ENVIRONMENT.md](ENVIRONMENT.md) - Variables de entorno

---

## 🆘 Necesitas Ayuda?

1. Lee la documentación en este repo
2. Revisa [CONTRIBUTING.md](CONTRIBUTING.md)
3. Abre un issue describiendo el problema
4. Contacta al equipo

---

**¡Happy coding! 🎉**
