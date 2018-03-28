import time
from threading import Thread
import Adafruit_PCA9685

class PCA9685:

    def __init__(self):
        self.pwm = Adafruit_PCA9685.PCA9685()

    def run(self):
        self.pwm.set_pwm_freq(60)

        while True:
            pwm.set_pwm(0, 0, 0)
            time.sleep(1)
            pwm.set_pwm(0, 4096, 4096)
            time.sleep(1)

    def start(self):
        print("Starting GPIO!")
        thread = Thread(target=self.run)
        thread.start()
