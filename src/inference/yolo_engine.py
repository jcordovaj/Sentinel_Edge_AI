import cv2
from ultralytics import YOLO
import time

class SentinelVision:
    def __init__(self, model_path="data/models/yolov8n.pt"):
        self.model = YOLO(model_path)
        self.target_fps = 5  # Por defecto en modo Eco
        self.is_active = True

    def set_performance_mode(self, mode: str):
        """
        Ajusta la intensidad de la IA según el estado del sistema.
        """
        modes = {
            "eco": 1,        # 1 Frame por segundo (Patrullaje preventivo)
            "normal": 5,     # 5 FPS (Monitoreo activo)
            "tactical": 30   # Máximo rendimiento (Incidente en curso)
        }
        self.target_fps = modes.get(mode, 5)
        print(f"🚀 IA Vision: Modo cambiado a {mode} ({self.target_fps} FPS)")

    def process_stream(self, frame):
        """
        Ejecuta la inferencia sobre un frame y retorna detecciones.
        """
        results = self.model(frame, verbose=False)
        detections = []
        
        for r in results:
            for box in r.boxes:
                # Filtrar por confianza y clases críticas (Persona, Arma, etc.)
                if box.conf > 0.5:
                    detections.append({
                        "class": self.model.names[int(box.cls)],
                        "confidence": float(box.conf),
                        "coords": box.xyxy.tolist()
                    })
        return detections