import pyaudio
import numpy as np
from pydub import AudioSegment
import random
import wave
import librosa
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Dimmer
import time
import random
import _thread

count = 1

y, sr = librosa.load("temp.wav")

tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
chunk_size = 6890  # int(((60 * sr) / 96))
print(chunk_size)

dmx = OpenDMXController()

fixture1 = dmx.add_fixture(Dimmer, name="Light1")
fixture2 = dmx.add_fixture(Dimmer, name="Light2")
fixture3 = dmx.add_fixture(Dimmer, name="Light3")
fixture4 = dmx.add_fixture(Dimmer, name="Light4")
fixture5 = dmx.add_fixture(Dimmer, name="Light5")
fixture6 = dmx.add_fixture(Dimmer, name="Light6")


def trigger_lights():
    global count
    print("Lights triggered!", count)
    count += 1


previous = 0.0


def analyze_audio(data):
    global previous
    global count
    global fixture3
    global on
    # Convert binary data to a NumPy array of integers
    audio_data = np.frombuffer(data, dtype=np.int16)

    audio_level = np.mean(np.abs(audio_data))
    print(audio_level)
    if (audio_level - previous) > 50:
        print(audio_level, previous,
              "----------------------------------------------------------------")
        
    else:
        print(audio_level, previous)
    previous = audio_level


# Initialize PyAudio
p = pyaudio.PyAudio()

# # Open a stream to play the audio
# mp3_file = "flicker.mp3"

# # Convert MP3 to WAV using pydub
# audio = AudioSegment.from_mp3(mp3_file)
# audio.export("temp2.wav", format="wav")


audio = wave.open("temp.wav", "rb")

stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                channels=audio.getnchannels(),
                rate=audio.getframerate(),
                output=True)

print("Playing audio...")

# Read audio data and analyze it in chunks
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
dmx.close()
