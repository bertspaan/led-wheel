from devices.io.gpio import GPIO
from devices.io.pca9685 import PCA9685

class Raspberry:

    def __init__(self, on_step):
        self.gpio = GPIO(on_step)
        self.pca9685 = PCA9685()

    def get_angle(self):
        return self.gpio.get_angle()

    def set_direction(self, direction):
        return self.gpio.set_direction(direction)

    def get_direction(self):
        return self.gpio.get_direction()

    def get_step(self):
        return self.gpio.get_step()

    def update_leds(self, leds):
        for index, value in enumerate(leds):
            self.pca9685.set_led(index, value)

    def start(self):
        self.gpio.start()
        self.pca9685.start()
