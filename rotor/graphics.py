
from programs import programs
from programs import effects

class Graphics:

    effects = {}
    program = None

    def __init__(self, led_count, transition=2000):
        self.led_count = led_count
        self.transition = transition

    # def set_program(name, parameter=None):
    #     if self.transition > 0:
    #
    #     else:
    #
    #

    def set_effect(name, value=0):
        if value > 0:
            self.effects[name] = value
        else:
            del self.effects[name]

    def calculate(self, angle):

        leds = [programs.programs['sine_wave']((360 / self.led_count * index + angle) % 360, 0.5) for index in range(self.led_count)]

        # led_count, wheel_angle, led_angle, parameter
        # print (programs.programs['single_light'](2))
        return leds
