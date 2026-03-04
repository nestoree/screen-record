# 🖥️ Screen & Audio Recorder (Python)
Este script de Python permite grabar de forma simultánea la pantalla y el audio del micrófono en un único archivo de vídeo .mp4. Detecta automáticamente múltiples monitores y dispositivos de audio para que el usuario elija cuáles usar.

## ✨ Características

- Detección de Hardware: Enumera todos los monitores y micrófonos conectados.
- Selección de Usuario: Interfaz por consola para elegir qué pantalla y qué micro grabar.
- Grabación Sincronizada: Utiliza hilos (threading) para capturar audio y vídeo a la vez.
- Salida Todo-en-Uno: Genera un archivo **.mp4** final con el audio integrado.

## 🚀 Instalación
- Clona o descarga este repositorio.
- Asegúrate de tener Python 3.8+ instalado.
- Instala las librerías necesarias ejecutando el siguiente comando en tu terminal:

```
pip install mss opencv-python pyaudio numpy screeninfo moviepy
```

Nota para usuarios de Windows: Si tienes problemas al instalar pyaudio, puedes descargar el .whl correspondiente desde aquí o instalarlo mediante 

```
pip install pipwin y luego pipwin install pyaudio.
```

## 🛠️ Cómo usarlo
Ejecuta el script principal:

```
python screen-record.py
```

- Selecciona tu monitor: Verás una lista de pantallas detectadas. Introduce el número (0, 1, etc.).
- Selecciona tu micrófono: Elige el dispositivo de entrada de audio de la lista.
- Grabación: El script empezará a grabar inmediatamente.
- Detener: Cuando quieras terminar, presiona **Ctrl + C** en la terminal.
- Procesamiento: Espera unos segundos a que el script combine el audio y el vídeo. El archivo final se guardará como grabacion_final.mp4.

## 📊 Flujo de Trabajo

⚠️ Notas Técnicas
- Archivos Temporales: El script crea archivos llamados temp_video.avi y temp_audio.wav durante la grabación. Se eliminan automáticamente al finalizar el proceso de unión.
- FPS: Por defecto, la grabación está configurada a 20 FPS para mantener un equilibrio entre calidad y rendimiento en Python.
- Rendimiento: Grabar pantalla en Python puro consume recursos de CPU. Se recomienda cerrar aplicaciones pesadas si notas "lag" en el vídeo resultante.

## 📄 Licencia
Este proyecto es de uso libre. ¡Siéntete libre de modificarlo y mejorarlo!
