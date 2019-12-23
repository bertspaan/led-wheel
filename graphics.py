import time
import math
from operator import add

from programs import programs
from programs import effects

class Graphics:

    effects = {
        'blur': 0,
        'motion_blur': 0,
        'strobe': 0,
        'dim': 0
    }

    program = 'fixed_one'
    previous_program = None
    last_program_change_ms = None

    parameter = 0.5
    bpm = 120

    beat = 0

    ceiling_led = 0
    ceiling_led_strobe = 0

    animation_angle = 0
    animation_rps = 0

    last_calculation_ms = 0

    def __init__(self, led_count, transition=500):
        self.led_count = led_count
        self.program_transition_ms = transition

    def set_ceiling_led(self, value):
        self.ceiling_led = value

    def set_ceiling_led_strobe(self, value):
        self.ceiling_led_strobe = value

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
        self.effects[name] = value

    def get_effects(self):
        return [(effect, round(value, 2)) for effect, value in self.effects.items()]

    def run_program(self, name, angle, beat):
        program = programs.programs[name]
        return [float(program((360 / self.led_count * index + angle + self.animation_angle) % 360, beat, self.parameter)) for index in range(self.led_count)]

    def apply_effects(self, leds, beat, ms):
        for effect, parameter in self.effects.items():
            leds = effects.effects[effect](leds, parameter, beat, ms)

        return leds

    def calculate(self, angle):
        ms = self.get_ms()
        diff_ms = ms - self.last_calculation_ms

        if self.last_program_change_ms is not None and self.last_program_change_ms + self.program_transition_ms < ms:
            self.previous_program = None

        self.animation_angle = self.animation_angle + diff_ms / 1000 * self.animation_rps * 360

        beat_duration = 1 / (self.bpm / 60) * 1000

        self.beat = self.beat + diff_ms / beat_duration
        beat = math.floor(self.beat)

        leds = self.run_program(self.program, angle, beat)

        if self.previous_program is not None:
            previous_leds = self.run_program(self.previous_program, angle, beat)
            ratio = round((ms - self.last_program_change_ms) / self.program_transition_ms, 3)
            leds = list(map(add, [ratio * led for led in leds], [(1 - ratio) * led for led in previous_leds]))

        leds = self.apply_effects(leds, beat, ms)
        self.last_calculation_ms = ms

        ceiling_leds = effects.effects['strobe']([self.ceiling_led], self.ceiling_led_strobe, beat, ms)

        return (leds, ceiling_leds[0])
