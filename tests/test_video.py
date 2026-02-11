"""
Script simple para probar el modelo con un video
Analiza el video frame por frame y genera estadísticas
"""

from ultralytics import YOLO
import cv2
from collections import defaultdict
import numpy as np
import os

def analyze_video(video_path, model_path='models/models_org/weights/best.pt'):
    """
    Analizar video completo y generar estadísticas por marca
    """
    
    if not os.path.exists(video_path):
        print(f"❌ Video no encontrado: {video_path}")
        print("\n💡 Para añadir un video:")
        print("   1. Descarga un video con logos desde YouTube:")
        print("      yt-dlp -f 'best[height<=720]' 'URL_VIDEO' -o 'tests/test_videos/%(title)s.%(ext)s'")
        print("\n   2. O graba tu propio video mostrando productos con logos")
        print("\n   3. Colócalo en: tests/test_videos/")
        return
    
    print(f"🎥 Analizando video: {video_path}")
    print("="*60)
    
    # Cargar modelo
    model = YOLO(model_path)
    
    # Abrir video
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"📊 Información del video:")
    print(f"   Duración: {duration:.2f}s")
    print(f"   FPS: {fps:.0f}")
    print(f"   Total frames: {total_frames}")
    print()
    
    # Estadísticas por marca
    brand_stats = defaultdict(lambda: {
        'frames': 0,
        'confidences': [],
        'first_appearance': None,
        'last_appearance': None
    })
    
    frame_count = 0
    frames_processed = 0
    
    print("🔍 Procesando video...")
    print("   (Analizando cada 5 frames para mayor velocidad)")
    print()
    
    # Preparar video de salida
    output_path = video_path.replace('.mp4', '_detected.mp4').replace('.avi', '_detected.avi')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    # Procesar cada frame
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Detectar cada N frames para acelerar
        if frame_count % 5 == 0:
            frames_processed += 1
            results = model(frame, verbose=False, conf=0.35)
            
            # Dibujar detecciones en el frame
            annotated_frame = results[0].plot()
            
            for r in results:
                for box in r.boxes:
                    brand = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    
                    # Actualizar estadísticas
                    brand_stats[brand]['frames'] += 1
                    brand_stats[brand]['confidences'].append(conf)
                    
                    if brand_stats[brand]['first_appearance'] is None:
                        brand_stats[brand]['first_appearance'] = frame_count / fps
                    brand_stats[brand]['last_appearance'] = frame_count / fps
            
            # Guardar frame anotado
            out.write(annotated_frame)
            
            # Mostrar progreso
            if frames_processed % 50 == 0:
                progress = frame_count / total_frames * 100
                print(f"   Progreso: {progress:.1f}% ({frame_count}/{total_frames} frames)")
        else:
            # Si no procesamos el frame, escribir el original
            out.write(frame)
        
        frame_count += 1
    
    cap.release()
    out.release()
    
    # Mostrar resultados
    print("\n" + "="*60)
    print("📊 RESULTADOS DEL ANÁLISIS")
    print("="*60)
    
    if not brand_stats:
        print("\n⚠️  No se detectaron logos en el video")
        print("\n💡 Sugerencias:")
        print("   - Usa un video con logos más visibles")
        print("   - Asegúrate de que las marcas estén en el dataset:")
        print("     Adidas, Apple, BMW, Coca Cola, Nike, Starbucks, etc.")
    else:
        for brand, stats in sorted(brand_stats.items(), key=lambda x: x[1]['frames'], reverse=True):
            time_seconds = stats['frames'] * 5 / fps  # *5 porque procesamos cada 5 frames
            percentage = (time_seconds / duration) * 100
            avg_conf = np.mean(stats['confidences'])
            
            print(f"\n🏷️  {brand}:")
            print(f"   Tiempo en pantalla: {time_seconds:.2f}s ({percentage:.1f}% del video)")
            print(f"   Confianza promedio: {avg_conf:.2%}")
            print(f"   Primera aparición: {stats['first_appearance']:.2f}s")
            print(f"   Última aparición: {stats['last_appearance']:.2f}s")
    
    print("\n" + "="*60)
    print(f"💾 Video con detecciones guardado en:")
    print(f"   {output_path}")
    print("="*60)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
    else:
        # Buscar primer video en tests/test_videos
        import glob
        videos = glob.glob('tests/test_videos/*.mp4')
        videos.extend(glob.glob('tests/test_videos/*.avi'))
        videos.extend(glob.glob('tests/test_videos/*.mov'))
        
        if videos:
            video_path = videos[0]
            print(f"📹 Usando video: {video_path}\n")
        else:
            print("❌ No se encontraron videos en tests/test_videos/")
            print("\n💡 Uso:")
            print("   python tests/test_video.py tests/test_videos/mi_video.mp4")
            print("\n   O coloca un video .mp4 en: tests/test_videos/")
            exit(1)
    
    analyze_video(video_path)
