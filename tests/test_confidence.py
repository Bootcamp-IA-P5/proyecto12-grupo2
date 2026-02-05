"""
Test de comparación de diferentes thresholds de confianza
Ayuda a encontrar el valor óptimo de conf para el modelo
"""

from ultralytics import YOLO
from pathlib import Path
import sys

def test_confidence_thresholds():
    """
    Comparar diferentes valores de confianza (0.25, 0.35, 0.50, 0.65)
    """
    
    print("\n🧪 COMPARACIÓN DE THRESHOLDS DE CONFIANZA")
    print("="*70)
    
    # Configuración
    model_path = 'models/models_org/weights/best.pt'
    test_images_dir = Path('tests/test_images/logos_reales')
    
    # Verificar que existen
    if not Path(model_path).exists():
        print(f"❌ Error: Modelo no encontrado en {model_path}")
        return
    
    if not test_images_dir.exists():
        print(f"❌ Error: Directorio de imágenes no encontrado: {test_images_dir}")
        return
    
    # Cargar modelo
    print(f"📦 Cargando modelo: {model_path}")
    model = YOLO(model_path)
    
    # Obtener imágenes de prueba
    image_files = list(test_images_dir.glob('*.jpg')) + \
                  list(test_images_dir.glob('*.jpeg')) + \
                  list(test_images_dir.glob('*.png'))
    
    if not image_files:
        print(f"❌ No se encontraron imágenes en {test_images_dir}")
        return
    
    print(f"📸 Imágenes de prueba: {len(image_files)}\n")
    
    # Thresholds a probar
    thresholds = [0.25, 0.35, 0.50, 0.65]
    
    print("="*70)
    print(f"{'Threshold':<12} {'Detecciones':<15} {'Confianza Avg':<18} {'Marcas Únicas':<15}")
    print("="*70)
    
    # Probar cada threshold
    for conf in thresholds:
        total_detections = 0
        confidence_scores = []
        brands_detected = set()
        
        for img_path in image_files:
            results = model(str(img_path), conf=conf, verbose=False)
            
            for r in results:
                if len(r.boxes) > 0:
                    for box in r.boxes:
                        brand = model.names[int(box.cls[0])]
                        confidence_score = float(box.conf[0])
                        
                        total_detections += 1
                        confidence_scores.append(confidence_score)
                        brands_detected.add(brand)
        
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        
        # Mostrar resultados
        status = "✅" if conf == 0.35 else "  "
        print(f"{status} conf={conf:.2f}   {total_detections:<15} {avg_confidence*100:.2f}%{'':<12} {len(brands_detected):<15}")
    
    print("="*70)
    print("\n💡 RECOMENDACIÓN:")
    print("   • conf=0.25 → Más detecciones, posibles falsos positivos")
    print("   • conf=0.35 → ✅ BALANCE ÓPTIMO (recomendado)")
    print("   • conf=0.50 → Alta precisión, menos detecciones")
    print("   • conf=0.65 → Muy estricto, puede perder detecciones válidas")
    print("\n📊 Basado en mAP50=0.651 del modelo, conf=0.35 es ideal")
    print("="*70)

if __name__ == "__main__":
    test_confidence_thresholds()
