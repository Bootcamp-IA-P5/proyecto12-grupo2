"""
Test con threshold más bajo para ver todas las detecciones posibles
"""
from ultralytics import YOLO
from pathlib import Path

def test_with_lower_confidence():
    """Test con conf=0.15 para ver qué detecta el modelo"""
    
    print("\n🧪 TEST CON THRESHOLD BAJO (conf=0.15)")
    print("="*70)
    
    model_path = 'models/models_org/weights/best.pt'
    test_images_dir = Path('tests/test_images/logos_reales')
    
    print(f"📦 Cargando modelo: {model_path}")
    model = YOLO(model_path)
    
    image_files = list(test_images_dir.glob('*.jpg')) + \
                  list(test_images_dir.glob('*.jpeg')) + \
                  list(test_images_dir.glob('*.png'))
    
    print(f"📸 Imágenes: {len(image_files)}\n")
    print("="*70)
    
    total_detections = 0
    images_with_detections = 0
    
    for img_path in sorted(image_files):
        print(f"\n📸 {img_path.name}")
        
        # Test con conf BAJO para ver qué puede detectar
        results = model(str(img_path), conf=0.15, save=True, 
                       project='runs/detect/tests', name='low_conf_test')
        
        detected = False
        for r in results:
            if len(r.boxes) > 0:
                detected = True
                images_with_detections += 1
                for box in r.boxes:
                    brand = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    total_detections += 1
                    
                    status = "✅" if conf > 0.35 else "⚠️" if conf > 0.25 else "🔴"
                    print(f"   {status} {brand}: {conf:.2%}")
        
        if not detected:
            print("   ❌ Sin detecciones (ni con conf=0.15)")
    
    print("\n" + "="*70)
    print("📊 RESUMEN CON conf=0.15")
    print("="*70)
    print(f"Imágenes con detecciones: {images_with_detections}/{len(image_files)}")
    print(f"Total detecciones: {total_detections}")
    print(f"Tasa de éxito: {images_with_detections/len(image_files)*100:.1f}%")
    print("="*70)
    
    print("\n💡 CONCLUSIÓN:")
    print("   Si aún así no hay detecciones → Las imágenes son muy diferentes")
    print("   del dataset de entrenamiento (Flickr27)")
    print("\n   SOLUCIÓN: Usar imágenes del tipo Flickr27 (logos en contexto)")

if __name__ == "__main__":
    test_with_lower_confidence()
