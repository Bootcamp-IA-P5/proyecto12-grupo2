"""
Script mejorado para descargar imágenes de prueba con logos en contexto
Usa URLs públicas de Wikimedia Commons y fuentes similares
"""

import urllib.request
import ssl
from pathlib import Path
import time

def download_image(url, filename, retry=3):
    """Descargar imagen con reintentos"""
    for attempt in range(retry):
        try:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            req = urllib.request.Request(url, headers=headers)
            
            with urllib.request.urlopen(req, context=ssl_context, timeout=15) as response:
                with open(filename, 'wb') as out_file:
                    out_file.write(response.read())
            
            return True
        except Exception as e:
            if attempt < retry - 1:
                print(f"   ⚠️  Intento {attempt + 1} falló, reintentando...")
                time.sleep(2)
            else:
                print(f"   ❌ Error después de {retry} intentos: {str(e)[:60]}")
                return False
    return False

def download_test_images():
    """
    Descargar imágenes de prueba con logos en contexto
    """
    
    print("\n📥 DESCARGANDO IMÁGENES DE PRUEBA CON LOGOS EN CONTEXTO")
    print("="*70)
    
    output_dir = Path('tests/test_images/flickr27_style')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs de imágenes con logos en contexto (fuentes públicas)
    # Usando imágenes de ejemplo de diferentes fuentes
    test_images = [
        # Nike - Logo en producto/contexto
        ("https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800", "nike_shoes_1.jpg"),
        
        # Starbucks - Taza en contexto
        ("https://images.unsplash.com/photo-1506619216599-9d16d0903dfd?w=800", "starbucks_cup_1.jpg"),
        
        # Apple - Logo en producto
        ("https://images.unsplash.com/photo-1611186871348-b1ce696e52c9?w=800", "apple_macbook_1.jpg"),
        
        # McDonald's - Restaurante
        ("https://images.unsplash.com/photo-1619454016518-697bc231e7ae?w=800", "mcdonalds_restaurant_1.jpg"),
        
        # Adidas - Producto/ropa
        ("https://images.unsplash.com/photo-1556906781-9a412961c28c?w=800", "adidas_shoes_1.jpg"),
        
        # Coca-Cola adicional
        ("https://images.unsplash.com/photo-1554866585-cd94860890b7?w=800", "cocacola_can_1.jpg"),
        
        # Pepsi
        ("https://images.unsplash.com/photo-1629203851122-3726ecdf080e?w=800", "pepsi_can_1.jpg"),
        
        # Nike adicional
        ("https://images.unsplash.com/photo-1605408499391-6368c628ef42?w=800", "nike_shoes_2.jpg"),
    ]
    
    print("🔄 Descargando imágenes de Unsplash (libre de derechos)...\n")
    
    downloaded = 0
    skipped = 0
    
    for url, filename in test_images:
        filepath = output_dir / filename
        
        # Verificar si ya existe
        if filepath.exists():
            print(f"⏭️  Ya existe: {filename}")
            skipped += 1
            continue
        
        print(f"📥 Descargando: {filename}")
        
        if download_image(url, filepath):
            file_size = filepath.stat().st_size / 1024
            print(f"   ✅ Guardado ({file_size:.1f} KB): {filepath.name}")
            downloaded += 1
        
        time.sleep(1)  # Pausa para no sobrecargar
    
    print("\n" + "="*70)
    print(f"📊 RESUMEN:")
    print(f"   Nuevas descargas: {downloaded}")
    print(f"   Ya existían: {skipped}")
    
    # Contar total de imágenes
    total_images = len(list(output_dir.glob('*.jpg'))) + \
                   len(list(output_dir.glob('*.jpeg'))) + \
                   len(list(output_dir.glob('*.png')))
    
    print(f"   Total en directorio: {total_images}")
    print(f"   Ubicación: {output_dir.absolute()}")
    
    if downloaded > 0:
        print("\n✅ ¡Imágenes descargadas! Ahora ejecuta:")
        print("   python tests/test_logo_images.py")
    
    if downloaded == 0 and skipped == 0:
        print("\n⚠️  No se pudieron descargar imágenes automáticamente.")
        print("   ALTERNATIVA: Descarga manualmente desde:")
        print("   • https://unsplash.com/s/photos/nike-shoes")
        print("   • https://unsplash.com/s/photos/starbucks-cup")
        print("   • https://unsplash.com/s/photos/brand-logos")
        print(f"\n   Guárdalas en: {output_dir.absolute()}")
    
    print("="*70)

if __name__ == "__main__":
    download_test_images()
