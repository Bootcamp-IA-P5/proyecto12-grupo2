"""
Script para evaluar el modelo YOLOv8 entrenado con diferentes imágenes y videos

Compatible con YOLOv8n, YOLOv8s, YOLOv8m y modelos personalizados entrenados con YOLOv8.
"""

from ultralytics import YOLO
import cv2
import os
from pathlib import Path
import json
from datetime import datetime
import numpy as np
from collections import defaultdict

class ModelEvaluator:
    def __init__(self, model_path, conf_threshold=0.35):
        """
        Inicializar evaluador con modelo YOLOv8 entrenado
        
        Args:
            model_path: Ruta al modelo best.pt (YOLOv8)
            conf_threshold: Umbral de confianza para detecciones (default: 0.35)
        """
        print(f"\n🔧 Cargando modelo YOLOv8: {model_path}")
        self.model = YOLO(model_path)
        self.conf_threshold = conf_threshold
        print(f"   Umbral de confianza: {self.conf_threshold}")
        self.results = {
            'model_path': model_path,
            'evaluation_date': datetime.now().isoformat(),
            'test_images': [],
            'test_videos': [],
            'summary': {}
        }
    
    def evaluate_single_image(self, image_path, save_dir='tests/results'):
        """
        Evaluar modelo YOLOv8 en una sola imagen
        
        Args:
            image_path: Ruta a la imagen
            save_dir: Directorio para guardar resultados
        """
        print(f"\n🖼️  Evaluando: {image_path}")
        
        # Hacer predicción con YOLOv8
        results = self.model(image_path, conf=self.conf_threshold, save=True, project=save_dir)
        
        # Analizar resultados
        image_result = {
            'image_path': image_path,
            'detections': []
        }
        
        for r in results:
            for box in r.boxes:
                detection = {
                    'brand': self.model.names[int(box.cls[0])],
                    'confidence': float(box.conf[0]),
                    'bbox': box.xyxy[0].tolist()
                }
                image_result['detections'].append(detection)
                print(f"   ✅ {detection['brand']}: {detection['confidence']:.2%}")
        
        if not image_result['detections']:
            print("   ⚠️  No se detectaron marcas")
        
        self.results['test_images'].append(image_result)
        return image_result
    
    def evaluate_directory(self, images_dir, save_dir='tests/results'):
        """
        Evaluar todas las imágenes en un directorio
        
        Args:
            images_dir: Directorio con imágenes
            save_dir: Directorio para guardar resultados
        """
        print(f"\n📁 Evaluando directorio: {images_dir}")
        
        # Extensiones soportadas
        extensions = ['.jpg', '.jpeg', '.png', '.bmp']
        
        image_files = []
        for ext in extensions:
            image_files.extend(Path(images_dir).glob(f'*{ext}'))
            image_files.extend(Path(images_dir).glob(f'*{ext.upper()}'))
        
        print(f"   Encontradas {len(image_files)} imágenes")
        
        for image_path in image_files:
            self.evaluate_single_image(str(image_path), save_dir)
    
    def evaluate_video(self, video_path, save_dir='tests/results', frame_skip=5):
        """
        Evaluar modelo YOLOv8 en un video
        
        Args:
            video_path: Ruta al video
            save_dir: Directorio para guardar resultados
            frame_skip: Procesar cada N frames para acelerar (default: 5)
        """
        print(f"\n🎥 Evaluando video: {video_path}")
        
        cap = cv2.VideoCapture(video_path)
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps
        
        print(f"   Duración: {duration:.2f}s | FPS: {fps:.0f} | Frames: {total_frames}")
        
        # Estadísticas por marca
        brand_stats = defaultdict(lambda: {
            'frames': 0,
            'confidences': [],
            'first_appearance': None,
            'last_appearance': None
        })
        
        frame_count = 0
        detections_per_frame = []
        
        # Procesar cada frame
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detectar cada N frames para acelerar
            if frame_count % frame_skip == 0:
                results = self.model(frame, conf=self.conf_threshold, verbose=False)
                
                frame_detections = []
                for r in results:
                    for box in r.boxes:
                        brand = self.model.names[int(box.cls[0])]
                        conf = float(box.conf[0])
                        
                        frame_detections.append({
                            'brand': brand,
                            'confidence': conf,
                            'frame': frame_count
                        })
                        
                        # Actualizar estadísticas
                        brand_stats[brand]['frames'] += 1
                        brand_stats[brand]['confidences'].append(conf)
                        
                        if brand_stats[brand]['first_appearance'] is None:
                            brand_stats[brand]['first_appearance'] = frame_count / fps
                        brand_stats[brand]['last_appearance'] = frame_count / fps
                
                detections_per_frame.append({
                    'frame': frame_count,
                    'detections': frame_detections
                })
            
            frame_count += 1
            
            # Mostrar progreso
            if frame_count % 100 == 0:
                print(f"   Procesados {frame_count}/{total_frames} frames ({frame_count/total_frames*100:.1f}%)")
        
        cap.release()
        
        # Calcular estadísticas finales
        video_result = {
            'video_path': video_path,
            'duration_seconds': duration,
            'total_frames': total_frames,
            'fps': fps,
            'brands_detected': {}
        }
        
        print("\n📊 Resultados:")
        for brand, stats in brand_stats.items():
            time_seconds = stats['frames'] * frame_skip / fps  # Ajustar por frame_skip
            percentage = (time_seconds / duration) * 100
            avg_conf = np.mean(stats['confidences'])
            
            video_result['brands_detected'][brand] = {
                'frames_detected': stats['frames'],
                'time_seconds': time_seconds,
                'percentage': percentage,
                'avg_confidence': avg_conf,
                'first_appearance': stats['first_appearance'],
                'last_appearance': stats['last_appearance']
            }
            
            print(f"   {brand}:")
            print(f"      Tiempo: {time_seconds:.2f}s ({percentage:.1f}% del video)")
            print(f"      Confianza promedio: {avg_conf:.2%}")
            print(f"      Primera aparición: {stats['first_appearance']:.2f}s")
        
        self.results['test_videos'].append(video_result)
        return video_result
    
    def generate_summary(self):
        """Generar resumen de todas las evaluaciones"""
        summary = {
            'total_images_tested': len(self.results['test_images']),
            'total_videos_tested': len(self.results['test_videos']),
            'brands_detected': set(),
            'average_confidence': []
        }
        
        # Analizar imágenes
        for img_result in self.results['test_images']:
            for det in img_result['detections']:
                summary['brands_detected'].add(det['brand'])
                summary['average_confidence'].append(det['confidence'])
        
        # Analizar videos
        for vid_result in self.results['test_videos']:
            for brand, stats in vid_result['brands_detected'].items():
                summary['brands_detected'].add(brand)
                summary['average_confidence'].append(stats['avg_confidence'])
        
        summary['brands_detected'] = list(summary['brands_detected'])
        if summary['average_confidence']:
            summary['average_confidence'] = float(np.mean(summary['average_confidence']))
        else:
            summary['average_confidence'] = 0.0
        
        self.results['summary'] = summary
        
        print("\n" + "="*60)
        print("📊 RESUMEN DE EVALUACIÓN")
        print("="*60)
        print(f"Imágenes evaluadas: {summary['total_images_tested']}")
        print(f"Videos evaluados: {summary['total_videos_tested']}")
        print(f"Marcas detectadas: {len(summary['brands_detected'])}")
        if summary['brands_detected']:
            print(f"   {', '.join(summary['brands_detected'])}")
        print(f"Confianza promedio: {summary['average_confidence']:.2%}")
        print("="*60)
        
        return summary
    
    def save_results(self, output_path='tests/results/evaluation_results.json'):
        """Guardar resultados en JSON"""
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n💾 Resultados guardados en: {output_path}")


def main():
    """Función principal de evaluación YOLOv8"""
    
    # Configuración del modelo YOLOv8
    # Opciones disponibles:
    # - 'models/models_mgg/weights/best.pt'  (YOLOv8s entrenado - Recomendado)
    # - 'models/models_org/weights/best.pt'  (YOLO11m entrenado)
    # - 'notebooks/yolov8n.pt'                (YOLOv8 nano - base)
    # - 'notebooks/yolov8s.pt'                (YOLOv8 small - base)
    # - 'notebooks/yolov8m.pt'                (YOLOv8 medium - base)
    
    model_path = 'models/models_mgg/weights/best.pt'  # Modelo YOLOv8s entrenado
    conf_threshold = 0.35  # Umbral de confianza (ajustar según necesidad: 0.25-0.50)
    
    if not os.path.exists(model_path):
        print(f"❌ Error: No se encuentra el modelo en {model_path}")
        print("\n💡 Modelos disponibles:")
        print("   - models/models_mgg/weights/best.pt (YOLOv8s entrenado)")
        print("   - models/models_org/weights/best.pt (YOLO11m entrenado)")
        print("   - notebooks/yolov8s.pt (YOLOv8 base)")
        return
    
    # Crear evaluador YOLOv8
    evaluator = ModelEvaluator(model_path, conf_threshold=conf_threshold)
    
    # 1. Evaluar imágenes individuales de prueba
    test_images_dir = 'tests/test_images'
    if os.path.exists(test_images_dir):
        evaluator.evaluate_directory(test_images_dir)
    else:
        print(f"⚠️  Directorio de imágenes no encontrado: {test_images_dir}")
        print("   Ejecuta primero: python tests/download_test_data.py")
    
    # 2. Evaluar videos de prueba
    test_videos_dir = 'tests/test_videos'
    if os.path.exists(test_videos_dir):
        video_files = list(Path(test_videos_dir).glob('*.mp4'))
        video_files.extend(list(Path(test_videos_dir).glob('*.avi')))
        video_files.extend(list(Path(test_videos_dir).glob('*.mov')))
        
        for video_path in video_files:
            evaluator.evaluate_video(str(video_path))
    else:
        print(f"⚠️  Directorio de videos no encontrado: {test_videos_dir}")
    
    # 3. Generar resumen
    evaluator.generate_summary()
    
    # 4. Guardar resultados
    evaluator.save_results()


if __name__ == "__main__":
    main()
