import time

from programs import programs
from programs import effects


# p1: fixed angle light 0
# p2: fixed angle light 0 + 15
# p3: fixed angle light elke drie
# p4: fixed angle light: eerste helft
# p5: 10, 20, 30 -> 5, 15, 25
# p6: 1-10, 11-20, 21-30
# p7: waaier
# p8: random beams

# snake

# k1: volume/parameter - lineair
# k2: chase speed: exp
# k3: animatiesnelheid: exp
# k4: dim ceiling
# k5: strobe: exp
# k6: blur
# k7:
# k8: dim all

class Graphics:

    effects = {}

    program = 'fan'
    previous_program = None
    last_program_change_ms = None
    program_transition_ms = 2000

    parameter = 0
    bpm = 120

    ceiling_led = 0

    animation_angle = 0
    animation_rps = 0

    last_calculation_ms = 0

    def __init__(self, led_count, transition=2000):
        self.led_count = led_count
        self.program_transition_ms = transition

    def set_ceiling_led(self, value):
        self.ceiling_led = value

    def get_ceiling_led(self):
        return self.ceiling_led

    def set_parameter(self, value):
        self.parameter = value

    def get_parameter(self):
        return self.parameter

    def set_program(self, name):
        if self.program_transition_ms > 0:
            self.previous_program = self.program
            self.last_program_change_ms = self.get_ms()

        self.program = name

    def set_bpm(self, value):
        self.bpm = value

    def get_bpm(self):
        return self.bpm

    def set_animation_rps(self, value):
        self.animation_rps = value

    def get_animation_rps(self):
        return self.animation_rps

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
        return [(effect, round(value, 2)) for effect, value in self.effects.items()]

    def apply_effects(self, leds, tick):
        for effect, parameter in self.effects.items():
            leds = effects.effects[effect](leds, parameter, tick)

        return leds

    def calculate(self, angle):
        ms = self.get_ms()
        diff_ms = ms - self.last_calculation_ms

        # if self.last_program_change_ms + self.program_transition_ms < ms:
        #     self.previous_program = None

        # if self.previous_program is not None:
        # self.previous_program = self.program
        # self.last_program_change_ms = self.get_ms()


        self.animation_angle = self.animation_angle + diff_ms / 1000 * self.animation_rps * 360
        program = programs.programs[self.program]


        beat_duration = (self.bpm / 60) / 2 * 1000
        tick = round(ms / beat_duration)


        leds = [float(program((360 / self.led_count * index + angle + self.animation_angle) % 360, tick, self.parameter)) for index in range(self.led_count)]
        leds = self.apply_effects(leds, tick)
        self.last_calculation_ms = ms
        return (leds, self.ceiling_led)
