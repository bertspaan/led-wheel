import time

from programs import programs
from programs import effects

class Graphics:

    effects = {
        # 'dim': 0.6,
        # 'strobe': 0.2
    }
    program = 'front'
    parameter = 0

    ceiling_led = 0

    animation_angle = 0
    animation_rps = 0.2
    last_calculation_ms = 0

    def __init__(self, led_count, transition=2000):
        self.led_count = led_count
        self.transition = transition

    def set_ceiling_led(self, value):
        self.ceiling_led = value

    def set_parameter(self, value):
        self.parameter = value

    def get_parameter(self):
        return self.parameter

    def set_program(self, name):
        self.program = name
    #     if self.transition > 0:
    #
    #     else:
    #
    #

    def get_program(self):
        return self.program

    def get_ms(self):
        return time.time() * 1000.0

    def set_effect(self, name, value=0):
        if value > 0:
            self.effects[name] = value
        else:
            del self.effects[name]

    def get_effects(self):
        return [(effect, value) for effect, value in self.effects.items()]

    def apply_effects(self, led):
        for effect, parameter in self.effects.items():
            led = effects.effects[effect](led, parameter)

        return led

    def calculate(self, angle):
        ms = self.get_ms()
        diff_ms = ms - self.last_calculation_ms

        self.animation_angle = self.animation_angle + diff_ms / 1000 * self.animation_rps * 360
        program = programs.programs[self.program]

        tick = 0
        parameter = 0

        leds = [program((360 / self.led_count * index + angle + self.animation_angle) % 360, tick, parameter) for index in range(self.led_count)]
        leds = map(self.apply_effects, leds)

        # led_count, wheel_angle, led_angle, parameter
        # print (programs.programs['single_light'](2))
        self.last_calculation_ms = ms
        return leds
