import pyttsx3
import speech_recognition as sr
import threading

class SentinelAudio:
    def __init__(self):
        # Inicializar el motor de síntesis de voz (Offline)
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150) # Velocidad de habla humana normal
        self.recognizer = sr.Recognizer()
        
    def whisper(self, text):
        """Envía una instrucción auditiva al guardia."""
        print(f"🎙️ Whispering: {text}")
        # Ejecutar en un hilo separado para no bloquear el procesamiento de video
        threading.Thread(target=self._say, args=(text,)).start()

    def _say(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen_command(self):
        """Escucha comandos cortos (SOS, Reportar, Refuerzos)."""
        with sr.Microphone() as source:
            print("🎤 Escuchando comando...")
            audio = self.recognizer.listen(source, phrase_time_limit=2)
            try:
                command = self.recognizer.recognize_google(audio, language="es-CL")
                return command.lower()
            except:
                return None