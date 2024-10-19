import pyaudio
import numpy as np
from pydub import AudioSegment
import wave
import librosa
import threading
import time
import random
from PyDMXControl.controllers import OpenDMXController
from PyDMXControl.profiles.Generic import Dimmer
import sys

LIGHT_DATA = {
    "fixture_1": None,
    "fixture_2": None,
    "fixture_3": None,
    "fixture_4": None,
    "fixture_5": None,
    "fixture_6": None,
}

dmx = OpenDMXController()

fixture1 = dmx.add_fixture(Dimmer, name="Light1")
fixture2 = dmx.add_fixture(Dimmer, name="Light2")
fixture3 = dmx.add_fixture(Dimmer, name="Light3")
fixture4 = dmx.add_fixture(Dimmer, name="Light4")
fixture5 = dmx.add_fixture(Dimmer, name="Light5")
fixture6 = dmx.add_fixture(Dimmer, name="Light6")


def trigger_lights(*argv):
    for index, fixture in enumerate(argv):
        LIGHT_DATA[f"fixture_{index+1}"] = int(fixture)
    # print(LIGHT_DATA)
    # print("\n\n\n")


def threading_function(fixture, fixture_number):
    while True:
        while LIGHT_DATA[f"fixture_{fixture_number}"] is None:
            time.sleep(0.1)
        # ACTAULLY CHANGE THE LIGHTS

        if LIGHT_DATA[f"fixture_{fixture_number}"] != -1:
            if fixture_number == 1:
                fixture6.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            elif fixture_number == 2:
                fixture5.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            elif fixture_number == 3:
                fixture4.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            elif fixture_number == 4:
                fixture3.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            elif fixture_number == 5:
                fixture2.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            elif fixture_number == 6:
                fixture1.dim(LIGHT_DATA[f"fixture_{fixture_number}"])
            else:
                pass

        LIGHT_DATA[f"fixture_{fixture_number}"] = None  # Reset the value


threads = []
for i in range(6):
    thread = threading.Thread(target=threading_function, args=("", i+1))
    threads.append(thread)
    thread.start()

CHUNK_SIZE = int(27562/1)  # int(((60 * sr) / 96))

count = 0.0
skip = False

GLOBAL_BEAT = 1
SECTION = 1
SECTION1_COUNTER = 1
SECTION2_COUNTER = 1
SECTION3_COUNTER = 0
SECTION5_COUNTER = 0
SECTION6_COUNTER = 0
SECTION7_COUNTER = 0
SECTION8_COUNTER = 0
SECTION9_COUNTER = 0
SECTION10_COUNTER = 0
COLOR = 1

UP = True
FOLLOW_COUNTER = 1


def analyze_audio(data):
    global count
    global skip
    global COLOR
    global SECTION1_COUNTER
    global SECTION2_COUNTER
    global SECTION3_COUNTER
    global SECTION5_COUNTER
    global SECTION6_COUNTER
    global SECTION7_COUNTER
    global SECTION8_COUNTER
    global SECTION9_COUNTER
    global SECTION10_COUNTER
    global SECTION
    global GLOBAL_BEAT
    global CHUNK_SIZE
    global UP
    global FOLLOW_COUNTER
    if skip == False:
        skip = True
        CHUNK_SIZE = int(27560/4)
        return

    if count in [1, 2, 3]:
        GLOBAL_BEAT += 1
        print("Count:" + str(count) + "----------------------------" +
              "Beat: " + str(GLOBAL_BEAT) + "     Sec:" + str(SECTION))

    if SECTION == 1:
        # NO MATTER BEAT, Pick colors 0-20 for all lights
        if count in [1, 2, 3]:
            trigger_lights(COLOR*35, COLOR*35, COLOR*35,
                           COLOR*35, COLOR*35, COLOR*35)
    elif SECTION == 2:
        if count == 1:
            if SECTION2_COUNTER == 1:
                # First Light
                # trigger_lights(0, 0, 0, 0, 0, 0)
                trigger_lights(COLOR, 0, 0, 0, 0, 0)
            elif SECTION2_COUNTER == 2:
                # First Light
                trigger_lights(COLOR, 0, 0, 0, 0, 0)
            elif SECTION2_COUNTER == 3:
                # Second Light
                trigger_lights(0, COLOR, 0, 0, 0, 0)
            elif SECTION2_COUNTER == 4:
                # Second Light
                trigger_lights(0, COLOR, 0, 0, 0, 0)
            elif SECTION2_COUNTER == 5:
                # Third Light
                trigger_lights(0, 0, COLOR, 0, 0, 0)
            elif SECTION2_COUNTER == 6:
                # Third Light
                trigger_lights(0, 0, COLOR, 0, 0, 0)
            elif SECTION2_COUNTER == 7:
                # Fourth Light
                trigger_lights(0, 0, 0, COLOR, 0, 0)
            elif SECTION2_COUNTER == 8:
                # Fourth Light
                trigger_lights(0, 0, 0, COLOR, 0, 0)
            else:
                pass
        elif count == 2:
            # Sixth Light
            trigger_lights(-1, -1, -1, -1, -1, COLOR)
        elif count == 3:
            # Fifth Light
            if SECTION2_COUNTER == 8:
                trigger_lights(-1, -1, -1, -1, COLOR, -1)
                SECTION2_COUNTER = 0
            else:
                trigger_lights(0, 0, 0, 0, 0, 0)
    elif SECTION == 3:
        if count == 1:
            if SECTION3_COUNTER in [0, 1]:
                # First Light
                # trigger_lights(0, 0, 0, 0, 0, 0)
                trigger_lights(20, 0, 0, 0, 0, 0)
            elif SECTION3_COUNTER == 2:
                # First Light
                trigger_lights(20, 0, 0, 0, 0, 0)
            elif SECTION3_COUNTER == 3:
                # Second Light
                trigger_lights(0, 20, 0, 0, 0, 0)
            elif SECTION3_COUNTER == 4:
                # Second Light
                trigger_lights(0, 20, 0, 0, 0, 0)
            elif SECTION3_COUNTER == 5:
                # Third Light
                trigger_lights(0, 0, 20, 0, 0, 0)
            elif SECTION3_COUNTER == 6:
                # Third Light
                trigger_lights(0, 0, 20, 0, 0, 0)
            elif SECTION3_COUNTER == 7:
                # Fourth Light
                trigger_lights(0, 0, 0, 20, 0, 0)
            elif SECTION3_COUNTER == 8:
                # Fourth Light
                trigger_lights(0, 0, 0, 20, 0, 0)
            else:
                pass
        elif (".0" in str(count) or ".5" in str(count)) and count != 3:
            COLOR = random.randint(2, 7)*35
            trigger_lights(-1, 0, 0, 0, 0, COLOR)
    elif SECTION == 4:
        if ".0" in str(count):
            trigger_lights(0, 0, COLOR, COLOR, 0, 0)
        elif ".25" in str(count):
            trigger_lights(0, COLOR, 0, 0, COLOR, 0)
        elif ".5" in str(count):
            trigger_lights(COLOR, 0, 0, 0, 0, COLOR)
        elif ".75" in str(count):
            COLOR = random.randint(2, 7)*35
            trigger_lights(COLOR, 0, 0, 0, 0, COLOR)
    elif SECTION == 5:
        if count == 1:
            if SECTION5_COUNTER == 1:
                # First Light
                # trigger_lights(0, 0, 0, 0, 0, 0)
                trigger_lights(20, COLOR, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 2:
                # First Light
                trigger_lights(20, COLOR, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 3:
                # Second Light
                trigger_lights(COLOR, 20, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 4:
                # Second Light
                trigger_lights(COLOR, 20, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 5:
                # Third Light
                trigger_lights(COLOR, COLOR, 20, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 6:
                # Third Light
                trigger_lights(COLOR, COLOR, 20, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 7:
                # Fourth Light
                trigger_lights(COLOR, COLOR, COLOR, 20, COLOR, COLOR)
            elif SECTION5_COUNTER == 8:
                # Fourth Light
                trigger_lights(COLOR, COLOR, COLOR, 20, COLOR, COLOR)
            else:
                pass
        elif count == 2:
            # Sixth Light
            trigger_lights(COLOR, COLOR, COLOR, COLOR, COLOR, 20)
        elif count == 3:
            # Fifth Light
            if SECTION5_COUNTER == 1:
                # First Light
                # trigger_lights(0, 0, 0, 0, 0, 0)
                trigger_lights(20, COLOR, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 2:
                # First Light
                trigger_lights(20, COLOR, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 3:
                # Second Light
                trigger_lights(COLOR, 20, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 4:
                # Second Light
                trigger_lights(COLOR, 20, COLOR, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 5:
                # Third Light
                trigger_lights(COLOR, COLOR, 20, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 6:
                # Third Light
                trigger_lights(COLOR, COLOR, 20, COLOR, COLOR, COLOR)
            elif SECTION5_COUNTER == 7:
                # Fourth Light
                trigger_lights(COLOR, COLOR, COLOR, 20, COLOR, COLOR)
            elif SECTION5_COUNTER == 8:
                # Fourth Light
                trigger_lights(COLOR, COLOR, COLOR, 20, COLOR, COLOR)
            else:
                pass
    elif SECTION == 6:
        COLOR = random.randint(1, 7)*35
        if FOLLOW_COUNTER == 1:
            trigger_lights(COLOR, 0, 0, 0, 0, 0)
        elif FOLLOW_COUNTER == 2:
            trigger_lights(0, COLOR, 0, 0, 0, 0)
        elif FOLLOW_COUNTER == 3:
            trigger_lights(0, 0, COLOR, 0, 0, 0)
        elif FOLLOW_COUNTER == 4:
            trigger_lights(0, 0, 0, COLOR, 0, 0)
        elif FOLLOW_COUNTER == 5:
            trigger_lights(0, 0, 0, 0, COLOR, 0)
        elif FOLLOW_COUNTER == 6:
            trigger_lights(0, 0, 0, 0, 0, COLOR)

        if FOLLOW_COUNTER == 6:
            FOLLOW_COUNTER -= 1
            UP = False
        elif FOLLOW_COUNTER == 1 and UP == False:
            FOLLOW_COUNTER += 1
            UP = True
        elif UP == True:
            FOLLOW_COUNTER += 1
        elif UP == False:
            FOLLOW_COUNTER -= 1
    elif SECTION == 7:
        COLOR = random.randint(1, 7)*35
        if ".0" in str(count):
            trigger_lights(COLOR, 0, 0, 0, 0, COLOR)
        elif ".25" in str(count):
            trigger_lights(0, COLOR, 0, 0, COLOR, 0)
        elif ".5" in str(count):
            trigger_lights(0, 0, COLOR, COLOR, 0, 0)
        elif ".75" in str(count):
            trigger_lights(COLOR, COLOR, COLOR, COLOR, COLOR, COLOR)
    elif SECTION == 8:
        if ".0" in str(count):
            trigger_lights(0, 0, COLOR, COLOR, 0, 0)
        elif ".25" in str(count):
            trigger_lights(0, COLOR, 0, 0, COLOR, 0)
        elif ".5" in str(count):
            trigger_lights(COLOR, 0, 0, 0, 0, COLOR)
        elif ".75" in str(count):
            COLOR = random.randint(2, 7)*35
            trigger_lights(COLOR, 0, 0, 0, 0, COLOR)

    elif SECTION == 9:
        trigger_lights(random.randint(1, 7)*35,
                       random.randint(1, 7)*35, random.randint(1, 7)*35, random.randint(1, 7)*35, random.randint(1, 7)*35, random.randint(1, 7)*35)
    elif SECTION == 10:
        trigger_lights(130, 130, 130, 130, 130, 130)

    if count == 3.75:
        count = 1.0
        if SECTION == 5:
            COLOR = random.randint(2, 7)*35
        elif SECTION == 6:
            COLOR = random.randint(1, 7)*35
        else:
            COLOR = random.randint(2, 7)*35
        if SECTION == 2:
            SECTION2_COUNTER += 1

        elif SECTION == 3:
            SECTION3_COUNTER += 1

        elif SECTION == 5:
            SECTION5_COUNTER += 1

        elif SECTION == 6:
            if SECTION6_COUNTER == 8:
                SECTION6_COUNTER = 0
            else:
                SECTION6_COUNTER += 1

        elif SECTION == 7:
            if SECTION7_COUNTER == 8:
                SECTION7_COUNTER = 0
            else:
                SECTION7_COUNTER += 1

        elif SECTION == 8:
            if SECTION8_COUNTER == 8:
                SECTION8_COUNTER = 0
            else:
                SECTION8_COUNTER += 1

        elif SECTION == 9:
            if SECTION9_COUNTER == 8:
                SECTION9_COUNTER = 0
            else:
                SECTION9_COUNTER += 1

        elif SECTION1_COUNTER == 1 and SECTION == 1:
            SECTION = 2
        elif SECTION == 1:
            SECTION1_COUNTER += 1
            COLOR += 1
    else:
        count += 0.25
        if SECTION == 1 and count in [1, 2, 3]:
            COLOR += 1

    if GLOBAL_BEAT == 28:
        SECTION = 3
    elif GLOBAL_BEAT == 52:
        SECTION = 4
    elif GLOBAL_BEAT == 67:
        SECTION = 5
    elif GLOBAL_BEAT == 85:
        SECTION = 6
        count = 1.0
    elif GLOBAL_BEAT == 133:
        SECTION = 7
    elif GLOBAL_BEAT == 109:
        SECTION = 8

    elif GLOBAL_BEAT == 157:
        SECTION = 9
    # elif GLOBAL_BEAT == 181:
    #     SECTION = 10
    elif GLOBAL_BEAT == 191:
        SECTION = 10


if __name__ == '__main__':
    try:
        p = pyaudio.PyAudio()
        audio = wave.open("assets/cfc.wav", "rb")

        stream = p.open(format=p.get_format_from_width(audio.getsampwidth()),
                        channels=audio.getnchannels(),
                        rate=audio.getframerate(),
                        output=True)

        trigger_lights(0, 0, 0, 0, 0, 0)

        print("Playing audio...")

        data = audio.readframes(CHUNK_SIZE)
        while data:
            stream.write(data)
            analyze_audio(data)
            data = audio.readframes(CHUNK_SIZE)

        print("Audio playback finished.")

        # Cleanup
        stream.stop_stream()
        stream.close()
        audio.close()
        p.terminate()
        dmx.close()
        sys.exit("Program Completed")
    except KeyboardInterrupt:
        print("\nExiting.")
