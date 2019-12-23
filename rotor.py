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
from devices.websockets_server import WebsocketsServer

from graphics import Graphics

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

        self.raspberry = Raspberry(self.on_step)
        self.websockets_server = WebsocketsServer(self.on_message)

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

        if message['type'] == 'program':
            program_id = message['id']
            # TODO: check if program_id exists!
            if program_id is not None:
                self.graphics.set_program(program_id)
            self.log()

        elif message['type'] == 'effect':
            effect_id = message['id']
            value = message['value']
            # TODO: check if effect_id exists!
            if effect_id is not None:
                self.graphics.set_effect(effect_id, value)
            self.log()

        elif message['type'] == 'parameter':
            parameter_id = message['id']
            value = message['value']

            # TODO: check if parameter_id exists!
            if parameter_id is not None:
                self.graphics.set_parameter(value)
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
        print('  Connections:', self.websockets_server.get_connection_count())
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
        self.websockets_server.start()

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
