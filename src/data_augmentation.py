# src/data_augmentation.py
import cv2
import numpy as np
from pathlib import Path

def apply_augmentation(image_path, output_folder):
    """
    Aplica las técnicas requeridas por la rúbrica y guarda los resultados.
    """
    # 1. Cargar imagen con Path para portabilidad
    img = cv2.imread(str(image_path))
    if img is None:
        print(f"❌ Error: No se pudo encontrar la imagen en {image_path}")
        return

    # Crear carpeta de salida si no existe
    output_folder.mkdir(parents=True, exist_ok=True)

    # --- TÉCNICA A: FLIP (Rúbrica: flip) ---
    flipped = cv2.flip(img, 1) # 1 = horizontal
    cv2.imwrite(str(output_folder / "sample_flip.jpg"), flipped)

    # --- TÉCNICA B: COLOR JITTER (Rúbrica: color jitter) ---
    # Ajustamos brillo y contraste
    jitter = cv2.convertScaleAbs(img, alpha=1.3, beta=40)
    cv2.imwrite(str(output_folder / "sample_jitter.jpg"), jitter)

    # --- TÉCNICA C: RANDOM CROP (Rúbrica: crop) ---
    h, w = img.shape[:2]
    start_y, start_x = h//4, w//4
    cropped = img[start_y:start_y+(h//2), start_x:start_x+(w//2)]
    cv2.imwrite(str(output_folder / "sample_crop.jpg"), cropped)

    print(f"✅ Pruebas completadas. Revisa la carpeta: {output_folder}")

# --- BLOQUE DE PRUEBA ---
if __name__ == "__main__":
    # Definimos rutas relativas al archivo actual
    BASE_DIR = Path(__file__).resolve().parent.parent
    IMAGE_TO_TEST = BASE_DIR / "data" / "test_samples" / "test_image.jfif"
    OUTPUT_PATH = BASE_DIR / "data" / "augmented_results"

    apply_augmentation(IMAGE_TO_TEST, OUTPUT_PATH)