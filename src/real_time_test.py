# src/real_time_test.py
import cv2
from ultralytics import YOLO

# Cargamos el modelo (recuerda usar la lógica de Path que arreglamos antes)
model = YOLO('models/models_org/weights/best.pt')

def start_real_time_detection():
    # Abrir la captura de video (0 suele ser la webcam integrada)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Realizar detección en tiempo real
        results = model(frame, stream=True)

        for r in results:
            annotated_frame = r.plot() # Dibujar cajas y etiquetas

        # Mostrar el resultado en una ventana
        cv2.imshow("KUMO VISION - Real Time", annotated_frame)

        # Salir con la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()

# ¡Atrévete a probarlo en la siguiente daily!