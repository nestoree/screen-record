import cv2
import numpy as np
import mss
import pyaudio
import wave
import threading
import os
import time
from screeninfo import get_monitors
from moviepy.editor import VideoFileClip, AudioFileClip

# Configuración de Audio
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100

def listar_recursos():
    monitores = get_monitors()
    print("\n--- SELECCIÓN DE PANTALLA ---")
    for i, m in enumerate(monitores):
        print(f"[{i}] {m.name} ({m.width}x{m.height})")
    
    p = pyaudio.PyAudio()
    print("\n--- SELECCIÓN DE MICRÓFONO ---")
    info = p.get_host_api_info_by_index(0)
    mics = []
    for i in range(info.get('deviceCount')):
        dev = p.get_device_info_by_host_api_device_index(0, i)
        if dev.get('maxInputChannels') > 0:
            print(f"[{len(mics)}] {dev.get('name')}")
            mics.append(i)
    return monitores, mics, p

def grabar_audio(idx_mic, p, stop_event):
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE,
                    input=True, input_device_index=idx_mic, frames_per_buffer=CHUNK)
    frames = []
    while not stop_event.is_set():
        frames.append(stream.read(CHUNK))
    
    stream.stop_stream()
    stream.close()
    
    with wave.open("temp_audio.wav", 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

def main():
    monitores, mics_indices, p = listar_recursos()
    
    m_idx = int(input("\nNúmero del MONITOR: "))
    mic_user_idx = int(input("Número del MICRÓFONO: "))
    
    monitor = monitores[m_idx]
    # mss usa un índice basado en 1 para monitores individuales
    sct_config = {"top": monitor.y, "left": monitor.x, "width": monitor.width, "height": monitor.height}
    
    # Nombre del archivo final
    filename = "grabacion_final.mp4"
    fps = 20.0
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_out = cv2.VideoWriter("temp_video.avi", fourcc, fps, (monitor.width, monitor.height))

    stop_event = threading.Event()
    audio_thread = threading.Thread(target=grabar_audio, args=(mics_indices[mic_user_idx], p, stop_event))

    print("\n>>> GRABANDO... Presiona Ctrl+C para detener.")
    audio_thread.start()
    
    start_time = time.time()
    frames_count = 0

    with mss.mss() as sct:
        try:
            while not stop_event.is_set():
                # Captura de pantalla
                img = sct.grab(sct_config)
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                video_out.write(frame)
                frames_count += 1
                
                # Control simple de FPS para evitar que el video vaya "acelerado"
                expected_frame = int((time.time() - start_time) * fps)
                while frames_count < expected_frame:
                    video_out.write(frame)
                    frames_count += 1
                    
        except KeyboardInterrupt:
            print("\nDeteniendo grabación...")
            stop_event.set()

    audio_thread.join()
    video_out.release()
    p.terminate()

    # --- UNIÓN DE ARCHIVOS ---
    print("Procesando archivo final (uninedo audio y video)...")
    video_clip = VideoFileClip("temp_video.avi")
    audio_clip = AudioFileClip("temp_audio.wav")
    
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(filename, codec="libx264", audio_codec="aac")

    # Limpieza de temporales
    video_clip.close()
    audio_clip.close()
    os.remove("temp_video.avi")
    os.remove("temp_audio.wav")
    
    print(f"\n¡Listo! Video guardado como: {filename}")

if __name__ == "__main__":
    main()