import pygame
import time
import threading

# Function to play the audio


def play_audio(audio_file):
    pygame.mixer.init()
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()

# Function to print "Hello" every 10 seconds


count = 1


def print_hello_interval(interval):
    global count
    while True:
        print(count)
        if count == 4:
            count = 1
        else:
            count += 1
        time.sleep(interval)


if __name__ == "__main__":
    audio_file = "CornfieldChase.mp3"  # Replace with the path to your audio file

    # Start playing the audio in a separate thread
    audio_thread = threading.Thread(target=play_audio, args=(audio_file,))
    audio_thread.start()

    # Start printing "Hello" every 10 seconds
    print_hello_interval((100/4)/60)

    # Wait for the audio thread to finish (or you can add other logic to stop it)
    audio_thread.join()
