# ✅ CHECKLIST DE VERIFICACIÓN - Sistema Completo

## Antes de Demostrar

### 1. Servicios Base ✓
```bash
# PostgreSQL
sudo service postgresql status
pg_isready -h localhost -p 5432

# Python venv
source .venv/bin/activate
which python  # Debe mostrar ruta en .venv
```

### 2. Modelo YOLO ✓
```bash
ls -lh models/models_org/weights/best.pt
# Debe existir el archivo del modelo
```

### 3. Base de Datos ✓
```bash
psql -U postgres -c "\l" | grep brandtracker
# Debe existir la base de datos brandtracker
```

### 4. Variables de Entorno ✓

**Archivo raíz `.env`:**
```bash
cat .env | grep POSTGRES
# Debe mostrar configuración de PostgreSQL
```

**Archivo `frontend/.env`:**
```bash
cat frontend/.env
# Debe tener VITE_API_URL=http://localhost:8001
```

### 5. Dependencias ✓

**Python:**
```bash
pip list | grep -E "fastapi|uvicorn|sqlalchemy|psycopg2"
```

**Node:**
```bash
cd frontend
npm list recharts
# Debe mostrar recharts@3.7.0
```

### 6. Build del Frontend ✓
```bash
cd frontend
npm run build
# Debe compilar sin errores
```

## Inicio del Sistema

### Opción A: Script Automático (Recomendado)
```bash
./start-full.sh
```

### Opción B: Manual en 2 Terminales

**Terminal 1 - Backend:**
```bash
source .venv/bin/activate
cd src/demo
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8001
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Verificación del Sistema

### 1. Backend Responde ✓
```bash
curl http://localhost:8001/model-info/
# Debe retornar JSON con marcas detectables
```

### 2. Frontend Carga ✓
```bash
curl http://localhost:5173/
# Debe retornar HTML
```

Abrir navegador en: http://localhost:5173

### 3. CORS Funciona ✓
Desde el navegador (F12 Console):
```javascript
fetch('http://localhost:8001/model-info/')
  .then(r => r.json())
  .then(d => console.log('✅ CORS OK:', d))
```

## Prueba Completa

### Test 1: YouTube URL
1. Ir a http://localhost:5173
2. Tab "🎬 New Analysis"
3. Botón "📺 YouTube URL"
4. Pegar URL de prueba
5. Click "🚀 Iniciar Análisis"
6. Verificar:
   - ✅ Barra de progreso funciona
   - ✅ Métricas se actualizan en tiempo real
   - ✅ Marcas detectadas aparecen
   - ✅ Al finalizar, muestra resultados

### Test 2: Archivo Local
1. Tab "📁 Subir Video"
2. Seleccionar archivo MP4 local
3. Click "🚀 Iniciar Análisis"
4. Verificar mismas cosas que Test 1

### Test 3: Visualización de Resultados
Después de un análisis exitoso:
- ✅ Tab "📊 Current Results" se activa
- ✅ Métricas principales visibles
- ✅ Gráfico de torta carga
- ✅ Tabla de marcas completa
- ✅ Galería de imágenes carga
- ✅ Click en imagen abre modal

### Test 4: Base de Datos
```bash
# Verificar que se guardó
psql -U postgres -d brandtracker -c "SELECT video_uuid, name, processed_at FROM videos ORDER BY processed_at DESC LIMIT 5;"

# Verificar detecciones
psql -U postgres -d brandtracker -c "SELECT brand_name, COUNT(*) FROM detections GROUP BY brand_name;"
```

### Test 5: Análisis Guardados
1. Tab "💾 Saved Analyses"
2. Debería listar análisis previos (una vez implementado el endpoint)

## Comandos de Diagnóstico

### Ver Logs Backend
```bash
tail -f /tmp/backend.log
```

### Ver Procesos Activos
```bash
# Backend
ps aux | grep uvicorn

# Frontend
ps aux | grep vite

# PostgreSQL
ps aux | grep postgres
```

### Limpiar y Reiniciar
```bash
# Matar procesos
pkill -f uvicorn
pkill -f vite

# Reiniciar PostgreSQL
sudo service postgresql restart

# Limpiar frontend
cd frontend
rm -rf node_modules dist
npm install
npm run build
```

## Métricas de Éxito

### Frontend
- ✅ Carga en < 2 segundos
- ✅ Sin errores en consola (F12)
- ✅ UI responsiva en mobile/desktop
- ✅ Animaciones suaves
- ✅ Gráficos se renderizan correctamente

### Backend
- ✅ Responde en < 100ms
- ✅ Streaming NDJSON funciona
- ✅ Sin errores 500
- ✅ CORS configurado
- ✅ Logs claros y útiles

### Base de Datos
- ✅ Análisis se guardan automáticamente
- ✅ Sin errores de conexión
- ✅ Queries son rápidas (< 500ms)
- ✅ Imágenes se almacenan correctamente

### Integración
- ✅ Frontend ↔ Backend: Sin errores
- ✅ Backend ↔ DB: Conexión estable
- ✅ Backend ↔ YOLO: Modelo carga correctamente
- ✅ Todo el flujo funciona end-to-end

## URLs para Demo

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Frontend UI | http://localhost:5173 | Interfaz principal |
| Backend API | http://localhost:8001 | API REST |
| API Docs | http://localhost:8001/docs | Documentación interactiva |
| ReDoc | http://localhost:8001/redoc | Docs alternativa |

## Datos de Prueba

### YouTube URLs (públicas para demo)
- Formula 1: https://www.youtube.com/watch?v=... (con logos de FedEx, DHL, etc)
- Fútbol: https://www.youtube.com/watch?v=... (con logos de Adidas, Nike)
- Eventos: Cualquier video con marcas visibles

### Videos Locales
- Ubicación: `data/test_samples/`
- Formatos: MP4, AVI, MOV, MKV
- Tamaño: < 100MB para pruebas rápidas

## Resultado Final Esperado

✅ **Frontend React completamente funcional**
✅ **Sin pantalla negra**
✅ **Análisis de videos funcionando**
✅ **Base de datos integrada**
✅ **Progreso en tiempo real**
✅ **Visualización con gráficos**
✅ **UI moderna y profesional**

## ¡Sistema Listo para Demostración! 🎉

Si todos los checks pasan:
- ✅ Frontend funciona
- ✅ Backend responde
- ✅ Base de datos conecta
- ✅ Análisis completo funciona

**El sistema está listo para producción.**
