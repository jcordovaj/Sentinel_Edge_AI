import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

def check_vms_health():
    url = os.getenv("DEV_LOCAL_SERVER_URL") + "/health"
    try:
        start_time = time.time()
        response   = requests.get(url, timeout=2)
        latency    = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            print(f"✅ Conectado al VMS (Latencia: {latency:.2f}ms)")
            return True
    except Exception as e:
        print("⚠️ VMS no alcanzable. Gatillando IA LOCAL (Modo Supervivencia)")
        return False

if __name__ == "__main__":
    check_vms_health()
