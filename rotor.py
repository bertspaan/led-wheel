#!/usr/bin/env python3

import os
import json
import atexit
import time
import math
from collections import deque
from functools import reduce
from blessings import Terminal

from devices.raspberry import Raspberry
from devices.web_client import WebClient

from graphics import Graphics
from controls import Controls

class Rotor:

    frame_durations = deque([1, 1], 20)
    fps = 200

    last_message = {}

    step = 0
    angle = 0

    def __init__(self, led_count):
        self.terminal = Terminal()
        print(self.terminal.enter_fullscreen)

        self.graphics = Graphics(led_count)
        self.controls = Controls() #config

        self.raspberry = Raspberry(self.on_step)
        self.web_client = WebClient(self.on_message)

    def on_step(self, step):
        self.step = step

    def on_message(self, message):
        self.last_message = message

        # message is of form:
        # {
        #   "type": "program|effect|parameter",
        #   "id": "program_id|effect_id|parameter_id",
        #   "value": "value"
        # }

        if message['event'] == 'pad':
            id = message['data']['id']
            program = self.controls.map_pad(id)
            if program is not None:
                self.graphics.set_program(program)

            self.log()
        elif message['event'] == 'knob':
            id = message['data']['id']
            message_value = message['data']['value']

            type, name, value = self.controls.map_knob(id, message_value)

            if type == 'parameter':
                self.graphics.set_parameter(value)
            elif type == 'bpm':
                bpm_min = 30
                bpm_max = 600
                self.graphics.set_bpm(round(bpm_min + value * (bpm_max - bpm_min)))
            elif type == 'effect':
                self.graphics.set_effect(name, value)
            elif type == 'animation_rps':
                animation_direction = -1 if value < 0 else 1
                rps = (1 - math.sqrt(1 - math.pow(value, 2))) * 4 * animation_direction
                self.graphics.set_animation_rps(rps)
            elif type == 'ceiling_led':
                if value <= 0:
                    self.graphics.set_ceiling_led(value + 1)
                    self.graphics.set_ceiling_led_strobe(0)
                else:
                    self.graphics.set_ceiling_led(1)
                    self.graphics.set_ceiling_led_strobe(1 - value * 0.8)

        elif message['event'] == 'rotation':
            direction = message['data']['direction']
            self.raspberry.set_direction(1 if direction == 'cw' else -1)

            self.log()

    def log(self):
        average_duration = reduce(lambda x, y: x + y, self.frame_durations) / len(self.frame_durations)
        rps = self.raspberry.get_rps()

        print(self.terminal.clear + 'Rotor!\n')
        print('  Direction:', 'clockwise' if self.raspberry.get_direction() == 1 else 'counterclockwise')
        print('  Angle:', round(self.raspberry.get_angle()))
        print('  Step:', self.raspberry.get_step())
        print('  Rotations per second:')
        print('    Step sensor:', round(rps[0], 2))
        print('    Rotation sensor:', round(rps[1], 2))

        print('Frames per second: ', round(1000 / average_duration, 2))

        print('WebSockets:')
        print('  Connections:', self.web_client.get_connection_count())
        print('  Last message:', self.last_message)

        print('Current program:')
        print(' ', self.graphics.get_program(), round(self.graphics.get_parameter(), 2))
        print('  Speed:', round(self.graphics.get_animation_rps(), 2), 'RPS')
        print('  BPM:', self.graphics.get_bpm())
        print('Effects:')
        print('  ', self.graphics.get_effects())
        print('Ceiling LED:', round(self.graphics.get_ceiling_led(), 2))


    def start(self):
        self.raspberry.start()
        self.web_client.start()

        frame = 0
        last = time.perf_counter()

        frame_ms = 1000 / self.fps

        while True:
            self.update()
            frame = (frame + 1) % 1000

            current = time.perf_counter()
            passed = round((current - last) * 1000, 2)

            self.frame_durations.appendleft(passed)

            if frame % (self.fps) == 0:
                self.log()

            if frame_ms - passed > 0:
                time.sleep((frame_ms - passed) / 1000)

            last = current

    def update(self):
        angle = self.raspberry.get_angle()
        leds, ceiling_led = self.graphics.calculate(angle)
        self.raspberry.update_leds(leds, ceiling_led)

def main():
    rotor = Rotor(30)
    rotor.start()

if __name__ == '__main__':
    main()
