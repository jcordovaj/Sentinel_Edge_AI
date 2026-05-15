# Cómo poner en marcha la emulación (Micro-escala)

Para que el laptop actúe como el "Centro de Comando y Control" y la bodycam pueda interactuar con él (reportes, instrucciones, transmisión de imágenes), siga estos pasos:

## Levantar el Servidor en forma local (Laptop, WS)

En una terminal, dentro de la carpeta sentinel-edge, y ejecuta:

```Bash

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor de emulación
uvicorn mock_server.server:app --reload --host 0.0.0.0 --port 8000
```

Nota: Al usar --host 0.0.0.0, el servidor será visible para tu celular si ambos están en la misma red Wi-Fi.
