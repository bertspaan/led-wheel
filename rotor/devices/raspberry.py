import time
from threading import Thread

from devices.io.gpio import GPIO

class Device:

    # def __init__(self):
        # doe iets!

    def run(self):
        while True:
            print("Hoi!")
            time.sleep(1)

    def start(self):
        thread = Thread(target=self.run)
        thread.start()
        thread.join()
