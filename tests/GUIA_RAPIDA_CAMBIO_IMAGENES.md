# 🚀 Guía Rápida: Cambiar Imágenes de Test a Flickr27-Style

## ✅ Cambios Realizados

### 1. Scripts Creados
- ✅ [tests/download_flickr27_test_images.py](tests/download_flickr27_test_images.py) - Descarga imágenes
- ✅ [tests/copy_val_images.py](tests/copy_val_images.py) - Copia del dataset
- ✅ [tests/test_with_lower_conf.py](tests/test_with_lower_conf.py) - Diagnóstico

### 2. Directorio Nuevo
- ✅ `tests/test_images/flickr27_style/` - Para imágenes en contexto

### 3. Actualizado
- ✅ [tests/test_logo_images.py](tests/test_logo_images.py#L16) - Ahora usa `flickr27_style/`
- ✅ [tests/test_images/README.md](tests/test_images/README.md) - Instrucciones detalladas

---

## 🎯 Próximos Pasos (ACCIÓN REQUERIDA)

### Paso 1: Descargar Imágenes con Logos en Contexto

**Opción A - Búsqueda Manual (5-10 minutos):**

1. Abre Google Images y busca:
   ```
   Nike logo shoes street photo
   Coca Cola bottle table real photo  
   Starbucks cup person holding
   BMW car real photo exterior
   McDonalds restaurant exterior photo
   Apple logo macbook real photo
   Adidas logo shirt person wearing
   Ferrari logo car real photo
   Pepsi can table real photo
   Puma logo shoes real photo
   ```

2. Descarga **~10 imágenes** (que sean fotos reales, no logos aislados)

3. Guárdalas en:
   ```
   tests/test_images/flickr27_style/
   ```

**Opción B - Kaggle Dataset (si lo tienes):**

```bash
# Si tienes el dataset Flickr27 en tu máquina
python tests/copy_val_images.py
```

---

### Paso 2: Ejecutar Pruebas

```bash
# Test con nuevas imágenes
python tests/test_logo_images.py

# Debería mostrar mejor tasa de éxito (60-80%)
```

---

## 📊 Resultados Esperados

### Antes (con logos_reales):
```
❌ Tasa de éxito: 7.7% (1/13)
❌ Detecciones incorrectas
❌ Confianza baja
```

### Después (con flickr27_style):
```
✅ Tasa de éxito: 60-80%
✅ Detecciones correctas
✅ Confianza promedio: 40-70%
```

---

## 🔍 Ejemplo de Imágenes Correctas

### ✅ SÍ usar (tipo Flickr27):
- 🏷️ Zapatillas Nike en pies de persona (calle/gimnasio)
- 🏷️ Lata de Coca-Cola en mesa con comida/bebidas
- 🏷️ Taza de Starbucks sostenida por manos
- 🏷️ Coche BMW en estacionamiento (logo visible)
- 🏷️ Restaurante McDonalds desde exterior
- 🏷️ MacBook con logo Apple en escritorio/cafetería
- 🏷️ Camiseta Adidas en persona (tienda/calle)

### ❌ NO usar:
- ❌ Logo Nike aislado, fondo blanco
- ❌ Logo vectorial de Coca-Cola solo
- ❌ Logo circular de Starbucks recortado
- ❌ Logo BMW sin contexto

---

## 💬 Resumen para Oscar

> **"He cambiado el sistema de pruebas para usar imágenes tipo Flickr27 (logos en contexto real). El test ahora busca en `flickr27_style/` en lugar de `logos_reales/`. Necesito descargar ~10 imágenes con logos en productos/escenas reales y guardarlas ahí. Con eso, la tasa de éxito debería subir de 8% a 60-80%."**

---

## 📁 Enlaces Rápidos

- **README detallado:** [tests/test_images/README.md](tests/test_images/README.md)
- **Análisis de problemas:** [tests/ANALISIS_RESULTADOS.md](tests/ANALISIS_RESULTADOS.md)
- **Test de confianza:** `python tests/test_confidence.py`
- **Diagnóstico:** `python tests/test_with_lower_conf.py`

---

📅 Actualizado: 5 de febrero de 2026
