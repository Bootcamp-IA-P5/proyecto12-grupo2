"""
Script para entrenar YOLOv11 localmente en CPU/GPU
ADVERTENCIA: En CPU tomará 8-12 horas. Se recomienda usar Google Colab con GPU.
"""

from ultralytics import YOLO
import time
import os

def train_local():
    """Entrenar modelo YOLOv11 localmente"""
    
    print("="*60)
    print("🏋️ ENTRENAMIENTO LOCAL DE YOLOv11")
    print("="*60)
    print("\n⚠️ ADVERTENCIA:")
    print("   Entrenar en CPU tomará 8-12 horas")
    print("   Se recomienda usar Google Colab con GPU (20-30 min)")
    print("\n¿Deseas continuar? (s/n): ", end="")
    
    respuesta = input().lower()
    if respuesta != 's':
        print("\n❌ Entrenamiento cancelado")
        print("   Usa Google Colab para entrenar más rápido")
        return
    
    # Verificar dataset
    dataset_path = 'data.yaml'
    if not os.path.exists(dataset_path):
        print(f"\n❌ Error: No se encuentra {dataset_path}")
        print("   Descarga el Flickr Logos 27 Dataset y crea data.yaml")
        return
    
    # Cargar modelo YOLOv11 nano
    print("\n📦 Cargando YOLOv11n...")
    model = YOLO('yolo11n.pt')
    
    # Configuración para CPU (ajustada)
    print("\n🏋️ Iniciando entrenamiento...\n")
    start_time = time.time()
    
    try:
        results = model.train(
            data=dataset_path,
            epochs=50,                    # Puedes reducir a 20-30 para probar
            imgsz=640,
            batch=4,                      # Batch pequeño para CPU
            workers=2,                    # Menos workers en CPU
            device='cpu',                 # Forzar CPU
            project='runs/detect',
            name='logos_local',
            patience=10,
            optimizer='AdamW',
            lr0=0.001,
            verbose=True,
            seed=42
        )
        
        # Tiempo total
        elapsed = time.time() - start_time
        hours = elapsed / 3600
        
        print("\n" + "="*60)
        print(f"✅ Entrenamiento completado en {hours:.1f} horas")
        print("="*60)
        
        # Ubicación del modelo
        model_path = 'runs/detect/logos_local/weights/best.pt'
        print(f"\n📁 Modelo guardado en: {model_path}")
        print("\nPróximos pasos:")
        print("1. Copiar modelo a: models/models_org/weights/best.pt")
        print("2. Ejecutar: python tests/model_evaluation/evaluate_model.py")
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Entrenamiento interrumpido por el usuario")
        print("   El modelo parcial se guardó en: runs/detect/logos_local/")
    except Exception as e:
        print(f"\n❌ Error durante el entrenamiento: {e}")

if __name__ == "__main__":
    train_local()
