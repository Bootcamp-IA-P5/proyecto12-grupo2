"""
Script para descargar imágenes de prueba tipo Flickr27
(logos en contexto real: productos, carteles, ropa, etc.)
"""

import urllib.request
import ssl
from pathlib import Path
import time

def download_image(url, filename):
    """Descargar imagen desde URL"""
    try:
        # Crear contexto SSL para evitar errores de certificado
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
        req = urllib.request.Request(url, headers=headers)
        
        with urllib.request.urlopen(req, context=ssl_context, timeout=10) as response:
            with open(filename, 'wb') as out_file:
                out_file.write(response.read())
        
        return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False

def download_flickr27_style_images():
    """
    Descargar imágenes de prueba con logos en contexto real
    Similar al dataset Flickr27
    """
    
    print("\n📥 DESCARGANDO IMÁGENES DE PRUEBA TIPO FLICKR27")
    print("="*70)
    print("💡 Logos EN CONTEXTO (productos, tiendas, personas, etc.)")
    print("="*70 + "\n")
    
    output_dir = Path('tests/test_images/flickr27_style')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs de imágenes con logos en contexto real
    # Usando Wikimedia Commons y fuentes de dominio público
    test_images = [
        # Nike - zapatillas/ropa en contexto
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/a/a6/Logo_NIKE.svg/800px-Logo_NIKE.svg.png", "nike_context_1.jpg"),
        
        # Coca-Cola - lata/botella en contexto
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/c/ce/Coca-Cola_logo.svg/800px-Coca-Cola_logo.svg.png", "cocacola_context_1.jpg"),
        
        # McDonald's - restaurante/producto
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/McDonald%27s_Golden_Arches.svg/800px-McDonald%27s_Golden_Arches.svg.png", "mcdonalds_context_1.jpg"),
        
        # Starbucks - taza/tienda
        ("https://upload.wikimedia.org/wikipedia/en/thumb/d/d3/Starbucks_Corporation_Logo_2011.svg/800px-Starbucks_Corporation_Logo_2011.svg.png", "starbucks_context_1.jpg"),
        
        # Apple - producto/dispositivo
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/f/fa/Apple_logo_black.svg/800px-Apple_logo_black.svg.png", "apple_context_1.jpg"),
        
        # Adidas - ropa/zapatillas
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/2/20/Adidas_Logo.svg/800px-Adidas_Logo.svg.png", "adidas_context_1.jpg"),
        
        # BMW - coche/concesionario
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/BMW.svg/800px-BMW.svg.png", "bmw_context_1.jpg"),
        
        # Pepsi - lata/botella
        ("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Pepsi_logo_2014.svg/800px-Pepsi_logo_2014.svg.png", "pepsi_context_1.jpg"),
        
        # Ferrari - coche/merchandising
        ("https://upload.wikimedia.org/wikipedia/en/thumb/d/d9/Scuderia_Ferrari_Logo.svg/800px-Scuderia_Ferrari_Logo.svg.png", "ferrari_context_1.jpg"),
        
        # Puma - ropa/zapatillas
        ("https://upload.wikimedia.org/wikipedia/en/thumb/4/49/Puma_logo.svg/800px-Puma_logo.svg.png", "puma_context_1.jpg"),
    ]
    
    print("⚠️  NOTA IMPORTANTE:")
    print("   Las URLs de Wikimedia tienen logos, pero son similares a los anteriores.")
    print("   Para mejores resultados, usa IMÁGENES CON CONTEXTO REAL.\n")
    print("📋 ALTERNATIVA RECOMENDADA:")
    print("   1. Busca en Google Images:")
    print("      • 'Nike shoes street photo'")
    print("      • 'Coca Cola bottle table real photo'")
    print("      • 'Starbucks cup person holding'")
    print("      • 'BMW car real photo'")
    print("      • 'McDonalds restaurant real photo'")
    print("   2. Guarda las imágenes manualmente en:")
    print(f"      {output_dir.absolute()}")
    print("   3. O usa el dataset de validación de Flickr27\n")
    
    print("="*70)
    print("🔄 Intentando descargar imágenes de ejemplo...\n")
    
    downloaded = 0
    for url, filename in test_images:
        filepath = output_dir / filename
        print(f"📥 Descargando: {filename}")
        
        if download_image(url, filepath):
            print(f"   ✅ Guardado en: {filepath}")
            downloaded += 1
        
        time.sleep(0.5)  # Pausa para no sobrecargar
    
    print("\n" + "="*70)
    print(f"📊 RESUMEN:")
    print(f"   Imágenes descargadas: {downloaded}/{len(test_images)}")
    print(f"   Directorio: {output_dir.absolute()}")
    
    if downloaded < len(test_images):
        print("\n⚠️  SIGUIENTE PASO:")
        print("   Descarga manualmente imágenes con CONTEXTO REAL y guárdalas en:")
        print(f"   {output_dir.absolute()}")
        print("\n   Busca fotos reales tipo:")
        print("   • Persona con camiseta Nike")
        print("   • Lata de Coca-Cola en mesa")
        print("   • Taza de Starbucks siendo sostenida")
        print("   • Coche BMW en la calle")
        print("   • Restaurante McDonalds (foto exterior)")
    
    print("="*70)

if __name__ == "__main__":
    download_flickr27_style_images()
