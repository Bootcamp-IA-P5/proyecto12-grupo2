"""
Script para descargar imágenes y videos de prueba con logos/marcas
"""

import os
from pathlib import Path
import requests
from urllib.parse import urlparse

def download_image(url, save_path):
    """Descargar imagen desde URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Descargada: {os.path.basename(save_path)}")
        return True
    except Exception as e:
        print(f"❌ Error descargando {os.path.basename(save_path)}: {e}")
        return False

def main():
    # Crear directorios
    os.makedirs('tests/test_images', exist_ok=True)
    os.makedirs('tests/test_videos', exist_ok=True)
    
    # URLs de imágenes de prueba con logos (Pexels - libre de derechos)
    # Nota: Estas URLs son de ejemplo y pueden cambiar. 
    # También puedes añadir tus propias imágenes manualmente en tests/test_images/
    test_images = {
        'adidas_store.jpg': 'https://images.pexels.com/photos/1598505/pexels-photo-1598505.jpeg?auto=compress&cs=tinysrgb&w=800',
        'nike_shoes.jpg': 'https://images.pexels.com/photos/2529148/pexels-photo-2529148.jpeg?auto=compress&cs=tinysrgb&w=800',
        'apple_products.jpg': 'https://images.pexels.com/photos/788946/pexels-photo-788946.jpeg?auto=compress&cs=tinysrgb&w=800',
        'coca_cola.jpg': 'https://images.pexels.com/photos/50593/coca-cola-cold-drink-soft-drink-coke-50593.jpeg?auto=compress&cs=tinysrgb&w=800',
        'starbucks.jpg': 'https://images.pexels.com/photos/324028/pexels-photo-324028.jpeg?auto=compress&cs=tinysrgb&w=800',
        'mcdonalds.jpg': 'https://images.pexels.com/photos/2251794/pexels-photo-2251794.jpeg?auto=compress&cs=tinysrgb&w=800',
        'shopping_brands.jpg': 'https://images.pexels.com/photos/1488463/pexels-photo-1488463.jpeg?auto=compress&cs=tinysrgb&w=800',
        'sports_logos.jpg': 'https://images.pexels.com/photos/274422/pexels-photo-274422.jpeg?auto=compress&cs=tinysrgb&w=800',
    }
    
    print("📥 Descargando imágenes de prueba con logos...")
    print("="*60)
    
    downloaded = 0
    for filename, url in test_images.items():
        save_path = os.path.join('tests/test_images', filename)
        
        # No descargar si ya existe
        if os.path.exists(save_path):
            print(f"⏭️  Ya existe: {filename}")
            continue
        
        if download_image(url, save_path):
            downloaded += 1
    
    print("="*60)
    print(f"\n✅ Descarga completada: {downloaded} imágenes nuevas")
    print(f"📁 Ubicación: tests/test_images/")
    
    # Información sobre videos
    print("\n" + "="*60)
    print("📹 Videos de prueba:")
    print("="*60)
    print("Puedes añadir videos manualmente en: tests/test_videos/")
    print("\nOpciones para obtener videos:")
    print("\n1. Descarga desde YouTube con yt-dlp:")
    print("   yt-dlp -f 'best[height<=720]' 'URL_VIDEO' -o 'tests/test_videos/%(title)s.%(ext)s'")
    print("\n2. Búsquedas recomendadas en YouTube:")
    print("   - 'commercial ads compilation'")
    print("   - 'brand logos sports'")
    print("   - 'logo detection test video'")
    print("   - 'brands in movies'")
    print("\n3. Videos de ejemplo (copia el enlace y usa yt-dlp):")
    print("   - Anuncios: https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    print("\n4. O graba tu propio video mostrando productos con logos")
    print("="*60)
    
    # Crear archivo README en test_images
    readme_path = 'tests/test_images/README.md'
    with open(readme_path, 'w') as f:
        f.write("""# Test Images

Este directorio contiene imágenes de prueba para evaluar el modelo de detección de logos.

## Añadir imágenes propias

Puedes añadir tus propias imágenes aquí. Formatos soportados:
- JPG/JPEG
- PNG
- BMP

## Fuentes recomendadas

- **Pexels**: https://www.pexels.com (libre de derechos)
- **Unsplash**: https://unsplash.com (libre de derechos)
- **Tus propias fotos**: Toma fotos de productos con logos

## Ejecutar evaluación

Después de añadir imágenes, ejecuta:

```bash
python tests/model_evaluation/evaluate_model.py
```
""")
    
    print(f"\n📄 Creado README en: {readme_path}")

if __name__ == "__main__":
    main()
