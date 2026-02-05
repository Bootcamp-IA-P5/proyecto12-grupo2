"""
Script para copiar imágenes del dataset de validación Flickr27
al directorio de pruebas (si el dataset está disponible)
"""

import shutil
from pathlib import Path
import random

def copy_validation_images_to_test():
    """
    Copiar imágenes del dataset de validación para usar en pruebas
    """
    
    print("\n📋 COPIANDO IMÁGENES DEL DATASET DE VALIDACIÓN")
    print("="*70)
    
    # Rutas
    val_images_dir = Path('data/images/val')
    test_dir = Path('tests/test_images/flickr27_style')
    
    # Verificar si existe el dataset de validación
    if not val_images_dir.exists():
        print(f"❌ No se encontró el dataset de validación en: {val_images_dir}")
        print("\n💡 OPCIONES:")
        print("\n1️⃣  Descargar el dataset Flickr27:")
        print("   • Visita: https://www.kaggle.com/datasets/rahmasleam/flickr27-dataset")
        print("   • O busca 'Flickr27 logo dataset' en Google")
        print("\n2️⃣  Descargar imágenes manualmente:")
        print("   • Busca en Google: 'Nike logo product photo'")
        print("   • Guarda en: tests/test_images/flickr27_style/")
        print("\n3️⃣  Usar imágenes de prueba de Google:")
        print(f"   • https://www.google.com/search?q=nike+logo+street+photo&tbm=isch")
        print(f"   • https://www.google.com/search?q=coca+cola+bottle+real+photo&tbm=isch")
        print(f"   • https://www.google.com/search?q=starbucks+cup+holding&tbm=isch")
        print(f"   • https://www.google.com/search?q=bmw+car+real+photo&tbm=isch")
        print(f"   • https://www.google.com/search?q=mcdonalds+restaurant+photo&tbm=isch")
        print("\n   Descarga ~10 imágenes y guárdalas en:")
        print(f"   {test_dir.absolute()}")
        print("="*70)
        return
    
    # Obtener lista de imágenes de validación
    image_files = list(val_images_dir.glob('*.jpg')) + \
                  list(val_images_dir.glob('*.jpeg')) + \
                  list(val_images_dir.glob('*.png'))
    
    if not image_files:
        print(f"❌ No se encontraron imágenes en: {val_images_dir}")
        return
    
    print(f"✅ Encontradas {len(image_files)} imágenes en el dataset de validación")
    print(f"📂 Copiando algunas imágenes de muestra a: {test_dir}\n")
    
    # Crear directorio de pruebas si no existe
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Seleccionar aleatoriamente 15 imágenes
    sample_images = random.sample(image_files, min(15, len(image_files)))
    
    copied = 0
    for img_path in sample_images:
        dest_path = test_dir / f"val_{img_path.name}"
        try:
            shutil.copy2(img_path, dest_path)
            print(f"✅ Copiado: {img_path.name} → {dest_path.name}")
            copied += 1
        except Exception as e:
            print(f"❌ Error copiando {img_path.name}: {e}")
    
    print("\n" + "="*70)
    print(f"📊 RESUMEN:")
    print(f"   Imágenes copiadas: {copied}")
    print(f"   Destino: {test_dir.absolute()}")
    print("\n✅ Ahora puedes ejecutar: python tests/test_logo_images.py")
    print("="*70)

if __name__ == "__main__":
    copy_validation_images_to_test()
