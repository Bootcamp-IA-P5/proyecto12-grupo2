"""
Script para descargar imágenes de prueba del tipo Flickr27
(logos en contexto real, no logos aislados)
"""

import os
import urllib.request
from pathlib import Path

def download_flickr27_test_images():
    """
    Descargar imágenes de ejemplo del tipo Flickr27
    (logos en contexto real: productos, edificios, ropa, etc.)
    """
    
    print("\n📥 DESCARGANDO IMÁGENES DE PRUEBA FLICKR27-STYLE")
    print("="*70)
    print("💡 Estas imágenes tienen logos EN CONTEXTO (como el dataset)")
    print("="*70 + "\n")
    
    output_dir = Path('tests/test_images/flickr27_style')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs de ejemplo con logos en contexto real (tipo Flickr27)
    # NOTA: Estas son URLs de ejemplo. Necesitas reemplazarlas con imágenes reales
    test_images = [
        # Ejemplo: Persona con camiseta de Nike en la calle
        # Ejemplo: Lata de Coca-Cola en una mesa
        # Ejemplo: Logo de Apple en un MacBook en uso
        # etc.
    ]
    
    print("⚠️  ACCIÓN REQUERIDA:")
    print("\n1. Busca imágenes en Google con estos términos:")
    print("   • 'Nike logo shirt street photo'")
    print("   • 'Coca-Cola can table real photo'")
    print("   • 'Starbucks cup person holding'")
    print("   • 'BMW logo car real photo'")
    print("   • 'McDonalds restaurant exterior'")
    print("\n2. Guarda las imágenes en:")
    print(f"   {output_dir.absolute()}")
    print("\n3. Asegúrate que sean:")
    print("   ✅ Fotos reales (no logos aislados)")
    print("   ✅ Logo visible pero en contexto")
    print("   ✅ Similar al dataset Flickr27")
    print("\n" + "="*70)

if __name__ == "__main__":
    download_flickr27_test_images()
