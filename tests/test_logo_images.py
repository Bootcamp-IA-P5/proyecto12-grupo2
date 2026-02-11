"""
Script rápido para probar el modelo con las imágenes nuevas de logos reales
"""

from ultralytics import YOLO
from pathlib import Path
import os

def test_logos():
    # Cargar modelo
    model_path = 'models/models_org/weights/best.pt'
    print(f"📦 Cargando modelo: {model_path}\n")
    model = YOLO(model_path)
    
    # Directorio con imágenes de logos en contexto (tipo Flickr27)
    images_dir = 'tests/test_images/flickr27_style'
    
    if not os.path.exists(images_dir):
        print(f"❌ Directorio no encontrado: {images_dir}")
        print("\n💡 INSTRUCCIONES:")
        print("   1. Descarga imágenes con logos EN CONTEXTO (tipo Flickr27)")
        print("   2. Busca en Google: 'Nike logo product photo', 'Starbucks cup', etc.")
        print(f"   3. Guárdalas en: {images_dir}")
        print("\n   O ejecuta: python tests/download_flickr27_test_images.py")
        return
    
    # Buscar todas las imágenes
    image_files = list(Path(images_dir).glob('*.jpg'))
    image_files.extend(list(Path(images_dir).glob('*.jpeg')))
    image_files.extend(list(Path(images_dir).glob('*.png')))
    
    print(f"🖼️  Encontradas {len(image_files)} imágenes\n")
    print("="*60)
    
    # Estadísticas
    total_detections = 0
    images_with_detections = 0
    
    # Probar cada imagen
    for img_path in sorted(image_files):
        print(f"\n📸 {img_path.name}")
        
        results = model(str(img_path), conf=0.35, save=True, project='runs/detect', name='logos_test')
        
        detected = False
        for r in results:
            if len(r.boxes) > 0:
                detected = True
                images_with_detections += 1
                for box in r.boxes:
                    brand = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    total_detections += 1
                    print(f"   ✅ {brand}: {conf:.2%}")
            
        if not detected:
            print(f"   ⚠️  Sin detecciones")
    
    # Resumen
    print("\n" + "="*60)
    print("📊 RESUMEN")
    print("="*60)
    print(f"Imágenes probadas: {len(image_files)}")
    print(f"Imágenes con detecciones: {images_with_detections}")
    print(f"Total de detecciones: {total_detections}")
    print(f"Tasa de éxito: {images_with_detections/len(image_files)*100:.1f}%")
    print("="*60)
    print(f"\n💾 Resultados guardados en: runs/detect/logos_test/")

if __name__ == "__main__":
    test_logos()
