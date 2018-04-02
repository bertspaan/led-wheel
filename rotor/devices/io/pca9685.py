import time
from threading import Thread
import math

io_available = False

try:
    import Adafruit_PCA9685
    io_available = True
except ModuleNotFoundError:
    print("Adafruit_PCA9685 not found, continuing regardless!")

class PCA9685:
    frequency = 1000
    ceiling = [1, 14]

    mapping = [
        [0, 0], # First of first PCA9685
        [0, 1],
        [0, 2],
        [0, 3],
        [0, 6],
        [0, 4],
        [0, 5],
        [0, 7],
        [0, 8],
        [0, 9],
        [0, 10],
        [0, 11],
        [0, 12],
        [0, 13],
        [0, 14],
        [1, 15], # First of second PCA9685
        [1, 13],
        [1, 12],
        [1, 11],
        [1, 10],
        [1, 9],
        [1, 8],
        [1, 7],
        [1, 6],
        [1, 5],
        [1, 4],
        [1, 3],
        [1, 2],
        [1, 1],
        [1, 0]
    ]

    def ease_in_exp(self, x):
        return pow(x, 1 / 0.5)

    def set_led(self, index, value):
        if not io_available:
            return

        led = self.mapping[index]

        max = 4095
        # value between 0 and 1
        on = 0
        off = round(max * self.ease_in_exp(value))

        pwm = self.pwms[led[0]]
        pwm.set_pwm(led[1], on, off)

    def run(self):
        for pwm in self.pwms:
            pwm.set_pwm_freq(self.frequency)

    def start(self):
        if not io_available:
            return

        self.pwms = [
            Adafruit_PCA9685.PCA9685(0x40),
            Adafruit_PCA9685.PCA9685(0x41)
        ]

        print("Starting PCA9685!")
        thread = Thread(target=self.run)
        thread.start()
