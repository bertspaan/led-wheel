import time
from threading import Thread

try:
    from gpiozero import Button
except RuntimeError:
    print("Error importing gpiozero!  This is probably because you need superuser privileges!")

class GPIO:

    def step(self):
        print("step!")

    def rotation(self):
        print("rotation!")

    def run(self):
       button1 = Button(18)
       button1.when_pressed = self.step

    def start(self):
        print("Starting GPIO!")
        thread = Thread(target=self.run)
        thread.start()
