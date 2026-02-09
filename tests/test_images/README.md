# 📸 Imágenes de Prueba para Detección de Logos

## 🎯 IMPORTANTE: Tipo de Imágenes Requeridas

El modelo **YOLOv11** fue entrenado con el dataset **Flickr27**, que contiene **logos en contexto real**:
- ✅ Fotos de productos (latas, botellas, ropa, coches, etc.)
- ✅ Logos visibles en escenas reales (tiendas, calles, eventos)
- ✅ Contexto ambiental (personas, mesas, edificios)

**NO usar:**
- ❌ Logos aislados/recortados con fondo blanco
- ❌ Logos vectoriales sin contexto
- ❌ Diseños gráficos

---

## 📂 Estructura de Directorios

```
tests/test_images/
├── logos_reales/          ❌ Logos aislados (tasa éxito: ~8%)
└── flickr27_style/        ✅ Logos en contexto (USAR ESTE)
```

---

## 📥 Cómo Obtener Imágenes de Prueba

### Opción 1: Descargar Manualmente (Recomendado) ⭐

**Busca en Google Images:**
- `Nike logo shoes street photo`
- `Coca Cola bottle table real photo`
- `Starbucks cup person holding`
- `BMW car real photo exterior`
- `McDonalds restaurant exterior photo`
- `Apple logo macbook real photo`

**Guárdalas en:** `tests/test_images/flickr27_style/`

### Opción 2: Usar Dataset de Validación

```bash
python tests/copy_val_images.py
```

### Opción 3: Fuentes Recomendadas

- **Pexels**: https://www.pexels.com (libre de derechos)
- **Unsplash**: https://unsplash.com (libre de derechos)
- **Flickr27**: https://www.kaggle.com/datasets/rahmasleam/flickr27-dataset

---

## 🧪 Ejecutar Pruebas

Después de añadir imágenes en `flickr27_style/`:

```bash
python tests/model_evaluation/evaluate_model.py
```
