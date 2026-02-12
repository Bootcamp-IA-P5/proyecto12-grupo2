# 🎤 KUMO VISION - Guía de Presentación Final

**Proyecto 12 - Grupo 2 - Bootcamp IA**  
**Fecha**: Febrero 2026

---

## 📊 Diapositiva 1: Portada

**KUMO VISION**  
*Sistema de Análisis de Exposición de Marcas*

- **Tecnología**: Computer Vision + Deep Learning
- **Modelo**: YOLOv8 entrenado en Flickr Logos Dataset
- **Stack**: FastAPI + React + PostgreSQL + Docker

**Equipo**: Grupo 2 - Bootcamp IA Uniminuto

---

## 🎯 Diapositiva 2: Problema y Solución

### El Problema
- Empresas necesitan medir exposición de marca en videos
- Análisis manual es costoso y lento
- Falta de métricas precisas en tiempo real

### Nuestra Solución
✅ **Detección automática** con YOLOv8  
✅ **Análisis en tiempo real** con streaming NDJSON  
✅ **3 tipos de input**: Videos locales, YouTube, Imágenes  
✅ **Dashboard interactivo** con métricas y gráficos  

---

## 🏗️ Diapositiva 3: Arquitectura

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Frontend  │────▶│   Backend    │────▶│  PostgreSQL │
│  React+Vite │     │    FastAPI   │     │  Database   │
│ Tailwind CSS│     │   YOLOv8     │     │   SQLAlchemy│
└─────────────┘     └──────────────┘     └─────────────┘
      ▲                    │
      │                    ▼
      │            ┌──────────────┐
      └────────────│  NDJSON      │
                   │  Streaming   │
                   └──────────────┘
```

**Flujo de Datos**:
1. Usuario sube video/imagen
2. Backend procesa con YOLO frame-by-frame
3. Streaming de progreso en tiempo real
4. Resultados guardados en PostgreSQL
5. Visualización con gráficos interactivos

---

## ✨ Diapositiva 4: Funcionalidades Principales

### 🎬 Análisis de Videos
- **Archivos locales**: MP4, AVI, MOV
- **YouTube URLs**: Descarga y análisis automático
- **Progreso en vivo**: Barra de progreso + timestamp actual

### 🖼️ Análisis de Imágenes
- **Detección instantánea** en fotos estáticas
- **Preview antes de analizar**
- **Resultados con bounding boxes**

### 📊 Dashboard de Resultados
- **Métricas**: Duración, exposición, visibilidad %
- **Gráfico de torta**: Distribución por marca
- **Detalles por marca**: Detecciones, tiempo, visibilidad
- **Sistema de guardado**: Control manual del usuario

---

## 🔧 Diapositiva 5: Stack Técnico

### Backend
- **FastAPI**: API REST con validación automática
- **YOLOv8**: Modelo de detección de objetos
- **PostgreSQL**: Base de datos relacional
- **SQLAlchemy**: ORM para Python
- **yt-dlp**: Descarga de videos YouTube

### Frontend
- **React 19**: Framework UI moderno
- **Vite**: Build tool ultra rápido
- **Tailwind CSS**: Framework de estilos utility-first
- **Recharts**: Librería de gráficos
- **NDJSON Streaming**: Progreso en tiempo real

### DevOps
- **Docker Compose**: Orquestación de contenedores
- **GitHub**: Versionado y colaboración
- **Nginx** (opcional): Reverse proxy

---

## 📈 Diapositiva 6: Demo en Vivo

### Flujo de Demostración

**1. Inicio (30 seg)**
```bash
docker-compose up
# Mostrar contenedores corriendo
```
- Frontend: http://localhost:5173
- Backend: http://localhost:9000
- Database: PostgreSQL en puerto 5432

**2. Análisis de Video (2 min)**
1. Tab "Nuevo análisis"
2. Seleccionar video con marcas Nike/Adidas
3. Mostrar progreso en tiempo real
4. Resultados con métricas y gráfico

**3. Análisis de Imagen (1 min)**
1. Tab "Analizar imagen"
2. Subir foto con logo visible
3. Detección instantánea
4. Mostrar resultados

**4. Guardado y Histórico (1 min)**
1. Botón "Guardar análisis"
2. Badge "✓ GUARDADO"
3. Tab "Análisis guardados"
4. Cargar análisis previo

---

## 📊 Diapositiva 7: Resultados y Métricas

### Casos de Uso Reales
- **Marketing**: Medir ROI de patrocinios
- **Medios**: Análisis de exposición en TV/streaming
- **Investigación**: Dataset de apariciones de marca
- **Compliance**: Verificar cumplimiento de contratos

### Métricas del Sistema
- **Velocidad**: ~1 frame/segundo en CPU
- **Precisión**: Depende del modelo YOLO entrenado
- **Escalabilidad**: Preparado para GPU (10-20x más rápido)
- **Formato**: Soporte para múltiples formatos video/imagen

---

## 🚀 Diapositiva 8: Mejoras Futuras

### Alta Prioridad
1. **Captura de frames**: Guardar imágenes con detecciones
2. **GPU Acceleration**: Cambiar a CUDA para mayor velocidad
3. **Batch Processing**: Procesar múltiples archivos en paralelo

### Media Prioridad
4. **Exportar reportes**: PDF/Excel con resultados
5. **Filtros avanzados**: Por marca, fecha, confianza
6. **Comparación**: Comparar múltiples análisis
7. **Dashboard empresarial**: Métricas agregadas

### Baja Prioridad
8. **Autenticación**: Login multi-usuario
9. **API rate limiting**: Control de carga
10. **Fine-tuning**: Entrenar modelo con marcas custom

---

## 💡 Diapositiva 9: Aprendizajes Clave

### Técnicos
- ✅ Integración YOLO con FastAPI
- ✅ Streaming NDJSON para UX fluida
- ✅ Docker Compose para desarrollo consistente
- ✅ React hooks para estado complejo
- ✅ PostgreSQL con SQLAlchemy ORM

### Soft Skills
- ✅ Trabajo en equipo distribuido
- ✅ Gestión de proyecto ágil
- ✅ Documentación exhaustiva
- ✅ Design thinking para UX

---

## 🎓 Diapositiva 10: Conclusiones

### Logros
✅ **Sistema completo end-to-end** funcionando en producción  
✅ **3 tipos de análisis**: Video local, YouTube, Imagen  
✅ **UI profesional** con branding KUMO VISION  
✅ **Base de datos** con histórico de análisis  
✅ **Dockerizado** y listo para deploy  
✅ **Documentación completa** para mantenimiento  

### Valor Entregado
- Sistema robusto para análisis de marca
- Dashboard intuitivo para usuarios no técnicos
- API REST documentada para integraciones
- Código limpio y bien estructurado
- Pipeline reproducible para MLOps

---

## 📞 Diapositiva 11: Contacto y Recursos

### Links del Proyecto
- **GitHub**: [Bootcamp-IA-P5/proyecto12-grupo2](https://github.com/Bootcamp-IA-P5/proyecto12-grupo2)
- **Documentación**: Ver carpeta `docs/`
- **Demo**: http://localhost:5173 (local)

### Documentos Clave
- [README.md](../README.md) - Guía principal
- [ACTUALIZACION_FINAL.md](ACTUALIZACION_FINAL.md) - Docs técnica completa
- [QUICKSTART.md](QUICKSTART.md) - Setup rápido

### Equipo
**Grupo 2** - Bootcamp IA Uniminuto  
Proyecto 12 - Computer Vision  
Febrero 2026

---

## 🎬 Script de Demo (5 minutos)

### Preparación (antes de presentar)
```bash
# Verificar que todo está corriendo
docker-compose ps

# Tener listo:
# - Video de prueba con marcas Nike/Adidas
# - Imagen con logo visible
# - Browser en http://localhost:5173
```

### Minuto 0-1: Introducción
> "KUMO VISION analiza exposición de marcas en videos e imágenes usando YOLOv8.  
> Tres formas de análisis: videos locales, YouTube, y fotos estáticas.  
> Todo en tiempo real con dashboard interactivo."

**Mostrar**: Pantalla de inicio con hero section

### Minuto 1-3: Demo Video
> "Voy a analizar este video de deportes con marcas visibles..."

**Acciones**:
1. Click tab "Nuevo análisis"
2. Seleccionar video
3. Click "Analizar"
4. **Mostrar progreso en vivo** (barra + timestamp)
5. Cuando termine: **señalar métricas, gráfico, detalles**

### Minuto 3-4: Demo Imagen
> "Ahora una imagen estática..."

**Acciones**:
1. Click tab "Analizar imagen"
2. Seleccionar imagen con logo
3. Mostrar preview
4. Click "Analizar imagen"
5. Resultados instantáneos

### Minuto 4-5: Guardado e Histórico
> "El usuario controla qué análisis guardar..."

**Acciones**:
1. Botón "Guardar análisis"
2. Badge "✓ GUARDADO" aparece
3. Click tab "Análisis guardados"
4. Mostrar lista
5. Cargar un análisis

**Cierre**:
> "Sistema completo, dockerizado, y listo para producción. ¿Preguntas?"

---

## 📋 Checklist Pre-Presentación

### Técnico
- [ ] `docker-compose up` funcionando
- [ ] Frontend carga sin errores
- [ ] Backend responde en /docs
- [ ] Database conectada
- [ ] Video de prueba preparado
- [ ] Imagen de prueba preparada

### Presentación
- [ ] Diapositivas preparadas
- [ ] Script de demo practicado
- [ ] Tiempos medidos
- [ ] Backup plan (screenshots si falla demo)
- [ ] Q&A anticipadas

### Entregables
- [ ] README actualizado
- [ ] Documentación en carpeta docs/
- [ ] Código en GitHub
- [ ] .gitignore configurado
- [ ] requirements.txt actualizado

---

**¡Éxito en la presentación! 🚀**
