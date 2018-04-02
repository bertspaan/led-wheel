import time

from programs import programs
from programs import effects

class Graphics:

    effects = {
        'dim': 0.6,
        'strobe': 0.2
    }
    program = None

    animation_angle = 0
    animation_rps = 0.4
    last_calculation_ms = 0

    def __init__(self, led_count, transition=2000):
        self.led_count = led_count
        self.transition = transition

    # def set_program(name, parameter=None):
    #     if self.transition > 0:
    #
    #     else:
    #
    #

    def get_ms(self):
        return time.time() * 1000.0

    def set_effect(name, value=0):
        if value > 0:
            self.effects[name] = value
        else:
            del self.effects[name]

    def apply_effects(self, led):
        for effect, parameter in self.effects.items():
            led = effects.effects[effect](led, parameter)

        return led

    def calculate(self, angle):
        ms = self.get_ms()
        diff_ms = ms - self.last_calculation_ms

        self.animation_angle = self.animation_angle + diff_ms / 1000 * self.animation_rps * 360
        program = programs.programs['sine_wave']
        leds = [program((360 / self.led_count * index + angle + self.animation_angle) % 360, 0.5) for index in range(self.led_count)]
        leds = map(self.apply_effects, leds)

        # led_count, wheel_angle, led_angle, parameter
        # print (programs.programs['single_light'](2))
        self.last_calculation_ms = ms
        return leds
