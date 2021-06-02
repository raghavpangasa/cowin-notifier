from pydub import AudioSegment
from playsound import playsound
import os

class Audio():
    def __init__(self):
        # print(os.system("ls"))
        print("")

    def play(self):
        try:
            playsound(".\\alert.mp3")
        except Exception as e:
            print(e)
            pass
        # print("playing")


