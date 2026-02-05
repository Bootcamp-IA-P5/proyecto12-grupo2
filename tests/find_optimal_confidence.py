"""
Script para encontrar el umbral de confianza óptimo para el modelo YOLOv11
Prueba diferentes valores de confianza y compara resultados
"""

from ultralytics import YOLO
from pathlib import Path
import json
from datetime import datetime
import os

def test_confidence_threshold(model_path, images_dir, confidence_values=[0.15, 0.25, 0.35, 0.50, 0.70]):
    """
    Probar diferentes umbrales de confianza y comparar resultados
    
    Args:
        model_path: Ruta al modelo best.pt
        images_dir: Directorio con imágenes de prueba
        confidence_values: Lista de umbrales a probar
    """
    
    print("🔬 EXPERIMENTO: Encontrar umbral de confianza óptimo")
    print("="*70)
    
    # Cargar modelo
    print(f"📦 Cargando modelo: {model_path}\n")
    model = YOLO(model_path)
    
    # Obtener imágenes
    image_files = []
    for ext in ['*.jpg', '*.jpeg', '*.png']:
        image_files.extend(list(Path(images_dir).glob(ext)))
    
    if not image_files:
        print(f"❌ No se encontraron imágenes en {images_dir}")
        return
    
    print(f"📸 Total de imágenes a probar: {len(image_files)}\n")
    
    # Resultados por umbral
    results_by_confidence = {}
    
    # Probar cada umbral
    for conf in confidence_values:
        print(f"\n{'='*70}")
        print(f"🎯 PROBANDO UMBRAL DE CONFIANZA: {conf:.0%}")
        print(f"{'='*70}")
        
        total_detections = 0
        images_with_detections = 0
        confidence_scores = []
        detections_per_brand = {}
        detections_per_image = []
        
        # Probar cada imagen
        for img_path in sorted(image_files):
            results = model(str(img_path), conf=conf, save=False, verbose=False)
            
            image_detections = 0
            for r in results:
                if len(r.boxes) > 0:
                    for box in r.boxes:
                        brand = model.names[int(box.cls[0])]
                        confidence_score = float(box.conf[0])
                        
                        total_detections += 1
                        image_detections += 1
                        confidence_scores.append(confidence_score)
                        
                        # Contar por marca
                        if brand not in detections_per_brand:
                            detections_per_brand[brand] = 0
                        detections_per_brand[brand] += 1
            
            if image_detections > 0:
                images_with_detections += 1
            
            detections_per_image.append({
                'image': img_path.name,
                'detections': image_detections
            })
        
        # Calcular métricas
        detection_rate = (images_with_detections / len(image_files)) * 100
        avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0
        avg_detections_per_image = total_detections / len(image_files)
        
        # Guardar resultados
        results_by_confidence[conf] = {
            'total_detections': total_detections,
            'images_with_detections': images_with_detections,
            'detection_rate': detection_rate,
            'avg_confidence': avg_confidence,
            'avg_detections_per_image': avg_detections_per_image,
            'detections_per_brand': detections_per_brand,
            'confidence_scores': confidence_scores,
            'detections_per_image': detections_per_image
        }
        
        # Mostrar resultados
        print(f"\n📊 RESULTADOS:")
        print(f"   Total detecciones: {total_detections}")
        print(f"   Imágenes con detección: {images_with_detections}/{len(image_files)}")
        print(f"   Tasa de detección: {detection_rate:.1f}%")
        print(f"   Confianza promedio: {avg_confidence:.1%}")
        print(f"   Detecciones por imagen: {avg_detections_per_image:.1f}")
        
        if detections_per_brand:
            print(f"\n   📋 Top 5 marcas detectadas:")
            sorted_brands = sorted(detections_per_brand.items(), key=lambda x: x[1], reverse=True)
            for brand, count in sorted_brands[:5]:
                print(f"      • {brand}: {count}")
    
    # COMPARACIÓN FINAL
    print(f"\n\n{'='*70}")
    print("📊 COMPARACIÓN DE TODOS LOS UMBRALES")
    print(f"{'='*70}\n")
    
    print(f"{'Umbral':<10} {'Detecciones':<15} {'Tasa %':<12} {'Conf. Prom':<15} {'Det/Img':<10}")
    print("-" * 70)
    
    for conf in confidence_values:
        r = results_by_confidence[conf]
        print(f"{conf:.0%}        "
              f"{r['total_detections']:<15} "
              f"{r['detection_rate']:<12.1f} "
              f"{r['avg_confidence']:<15.1%} "
              f"{r['avg_detections_per_image']:<10.1f}")
    
    # RECOMENDACIÓN
    print(f"\n{'='*70}")
    print("💡 RECOMENDACIÓN")
    print(f"{'='*70}\n")
    
    # Encontrar mejor balance
    best_conf = None
    best_score = 0
    
    for conf, r in results_by_confidence.items():
        # Puntuación: balance entre tasa de detección y confianza promedio
        # Penalizar mucho si la confianza promedio es baja (posibles falsos positivos)
        score = r['detection_rate'] * 0.4 + r['avg_confidence'] * 100 * 0.6
        
        if score > best_score:
            best_score = score
            best_conf = conf
    
    print(f"🎯 UMBRAL RECOMENDADO: {best_conf:.0%}")
    print(f"\n   Razón: Mejor balance entre detección y confianza")
    print(f"   • Detecciones totales: {results_by_confidence[best_conf]['total_detections']}")
    print(f"   • Tasa de detección: {results_by_confidence[best_conf]['detection_rate']:.1f}%")
    print(f"   • Confianza promedio: {results_by_confidence[best_conf]['avg_confidence']:.1%}")
    
    # Análisis adicional
    print(f"\n📌 ANÁLISIS:")
    print(f"   • Umbral MÁS PERMISIVO ({min(confidence_values):.0%}):")
    print(f"     - Detecta MÁS logos pero puede tener falsos positivos")
    print(f"     - {results_by_confidence[min(confidence_values)]['total_detections']} detecciones")
    
    print(f"\n   • Umbral MÁS ESTRICTO ({max(confidence_values):.0%}):")
    print(f"     - Detecta MENOS logos pero con mayor certeza")
    print(f"     - {results_by_confidence[max(confidence_values)]['total_detections']} detecciones")
    
    # Guardar resultados en JSON
    output_file = 'tests/results/confidence_threshold_experiment.json'
    os.makedirs('tests/results', exist_ok=True)
    
    experiment_data = {
        'date': datetime.now().isoformat(),
        'model_path': model_path,
        'images_dir': images_dir,
        'total_images': len(image_files),
        'confidence_values_tested': confidence_values,
        'results_by_confidence': {
            str(k): {
                'total_detections': v['total_detections'],
                'images_with_detections': v['images_with_detections'],
                'detection_rate': v['detection_rate'],
                'avg_confidence': v['avg_confidence'],
                'avg_detections_per_image': v['avg_detections_per_image'],
                'detections_per_brand': v['detections_per_brand']
            }
            for k, v in results_by_confidence.items()
        },
        'recommended_threshold': best_conf
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(experiment_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Resultados guardados en: {output_file}")
    
    return results_by_confidence, best_conf


if __name__ == "__main__":
    # Configuración
    MODEL_PATH = 'models/models_org/weights/best.pt'
    IMAGES_DIR = 'tests/test_images/logos_reales'
    
    # Umbrales a probar
    CONFIDENCE_THRESHOLDS = [0.15, 0.25, 0.35, 0.50, 0.70]
    
    # Ejecutar experimento
    test_confidence_threshold(MODEL_PATH, IMAGES_DIR, CONFIDENCE_THRESHOLDS)
