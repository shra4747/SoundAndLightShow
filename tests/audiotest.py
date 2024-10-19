import pyaudio
import numpy as np
from pydub import AudioSegment
import wave
import librosa
import threading
import time

count = 0
chunk_size = 27562


def analyze_audio(data):
    global count
    print("Beat", "\n\n\n" + "--------------------------" + str(count))
    if count == 3:
        count = 1        
    else:
        count += 1


if __name__ == '__main__':
    try:

        p = pyaudio.PyAudio()
        audio = wave.open("assets/cfc.wav", "rb")


        stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                        channels=audio.getnchannels(),
                        rate=audio.getframerate(),
                        output=True)

        print("Playing audio...")

        data = audio.readframes(chunk_size)
        while data:
            stream.write(data)
            analyze_audio(data)  # Analyze the audio data for triggering lights
            data = audio.readframes(chunk_size)

        print("Audio playback finished.")

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.close()
        p.terminate()

    except KeyboardInterrupt:
        print("Exiting.")
