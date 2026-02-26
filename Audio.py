import cv2
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np
import threading
import os
from datetime import datetime
import subprocess

# Create folder 
output_folder = "recordings"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Audio settings
fs = 44100  # Sample rate
audio_data = []
recording = False

def record_audio():
    global audio_data, recording
    audio_data = []

    def callback(indata, frames, time, status):
        if recording:
            audio_data.append(indata.copy())

    with sd.InputStream(samplerate=fs, channels=1, callback=callback):
        while recording:
            sd.sleep(100)

# Video setup
cap = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'XVID')

print("Press 's' to START recording")
print("Press 'e' to STOP recording")
print("Press 'q' to QUIT")

out = None
timestamp = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Interview Recorder", frame)
    key = cv2.waitKey(1) & 0xFF

    # Start
    if key == ord('s') and not recording:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_filename = os.path.join(output_folder, f"{timestamp}.avi")
        audio_filename = os.path.join(output_folder, f"{timestamp}.wav")

        out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))

        recording = True
        audio_thread = threading.Thread(target=record_audio)
        audio_thread.start()

        print("Recording started...")

    # Stop
    elif key == ord('e') and recording:
        recording = False
        audio_thread.join()
        out.release()

        # Save audio
        audio_np = np.concatenate(audio_data, axis=0)
        write(audio_filename, fs, audio_np)

        print("Recording stopped. Merging...")

        final_output = os.path.join(output_folder, f"{timestamp}_final.mp4")
        ffmpeg_path = r"C:\Users\HP\Downloads\ffmpeg-8.0.1-essentials_build\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

        subprocess.run([
            ffmpeg_path,
            "-y",
            "-i", video_filename,
            "-i", audio_filename,
            "-c:v", "libx264",
            "-c:a", "aac",
            final_output
        ])

        print("Saved:", final_output)

    # Quit
    elif key == ord('q'):
        break

    if recording:
        out.write(frame)

cap.release()
cv2.destroyAllWindows()