import cv2
import os
import sys
import json
import time
from dotenv import load_dotenv

# Asegurar que el directorio raíz del repositorio esté en sys.path
repo_root = os.path.dirname(os.path.abspath(__file__))
if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

# Importaciones de nuestros módulos
from src.core.daemon import NetworkDaemon
from src.core.crypto import SentinelCrypto
from src.inference.yolo_engine import SentinelVision
from src.utils.audio_tactical import SentinelAudio

load_dotenv()

def sentinel_boot():
    # Inicialización de hardware y software
    daemon = NetworkDaemon()
    crypto = SentinelCrypto()
    vision = SentinelVision()  # Carga yolov8n.pt
    audio  = SentinelAudio()
    
    # Simulador de Bodycam
    cap    = cv2.VideoCapture(0)
    
    print("--- SENTINEL EDGE ONLINE ---")
    audio.whisper("Sistema Sentinel iniciado. Modo patrullaje activo.")

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            # 1. Chequeo de Red
            is_connected = daemon.monitor_connectivity()
            
            # 2. Ajuste de rendimiento por contexto
            if not is_connected:
                vision.set_performance_mode("tactical")
            else:
                vision.set_performance_mode("eco")

            # 3. Inferencia de Visión
            detections = vision.process_stream(frame)

            # 4. Lógica de Respuesta Inmediata (Caso de Uso: Seguridad Pública)
            for det in detections:
                if det['class'] in ['knife', 'pistol', 'weapon']: # Clases YOLO
                    # Acción Criptográfica (Cadena de Custodia)
                    event = crypto.sign_event("AMENAZA_DETECTADA", frame.tobytes())
                    
                    # Acción Táctica (Audio)
                    audio.whisper("Amenaza detectada. Inicie protocolo defensivo. Desenfunde autorizado.")
                    
                    # Guardado Local Inmutable
                    with open(f"data/secure_vault/alert_{int(time.time())}.json", "w") as f:
                        json.dump(event, f)

            # 5. Interfaz de desarrollo
            cv2.imshow('Sentinel-Edge Viewport', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'): break

    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    sentinel_boot()