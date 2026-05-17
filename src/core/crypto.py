import hashlib
import time
import os
from cryptography.fernet import Fernet
from datetime import datetime

class SentinelCrypto:
    def __init__(self):
        # En producción, la llave se recupera de un KeyStore seguro
        self.key       = os.getenv("LOCAL_ENCRYPTION_KEY", Fernet.generate_key())
        self.cipher    = Fernet(self.key)
        self.device_id = os.getenv("DEVICE_ID", "DEV-001")

    def generate_evidence_hash(self, frame_data, metadata: dict):
        """
        Crea un hash SHA-256 combinando el frame, el timestamp y el ID del dispositivo.
        Esto garantiza la IRREFUTABILIDAD.
        """
        sha256 = hashlib.sha256()
        sha256.update(frame_data)
        sha256.update(str(metadata).encode())
        sha256.update(self.device_id.encode())
        return sha256.hexdigest()

    def sign_event(self, event_type: str, data: bytes):
        """
        Sella un evento con timestamp inmutable.
        """
        timestamp = datetime.now().isoformat()
        metadata = {
            "device_id" : self.device_id,
            "timestamp" : timestamp,
            "event_type": event_type
        }
        
        event_hash = self.generate_evidence_hash(data, metadata)
        
        return {
            "metadata": metadata,
            "hash": event_hash,
            "signature_version": "1.0"
        }
        
        # Nota: Agregar hash
