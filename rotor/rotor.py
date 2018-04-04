#!/usr/bin/env python3

import os
import json
import atexit
import time
from collections import deque
from functools import reduce
from blessings import Terminal

from devices.raspberry import Raspberry
from devices.web_client import WebClient

from graphics import Graphics
from controls import Controls

class Rotor:

    frame_durations = deque([], 20)
    fps = 60

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

    def on_step(self, step, angle):
        self.step = step
        self.angle = angle
        self.log()

    def on_message(self, message):
        self.last_message = message

        if message['event'] == 'pad':
            id = message['data']['id']
            program = self.controls.map_pad(id)
            if program is not None:
                self.graphics.set_program(program)
        elif message['event'] == 'knob':
            id = message['data']['id']
            message_value = message['data']['value']
            self.controls.map_knob(id, message_value)
            # type, value = self.controls.map_knob(id, message_value)
        elif message['event'] == 'rotation':
            direction = message['data']['direction']
            self.raspberry.set_direction(1 if direction == 'cw' else -1)

        self.log()

    def log(self):
        average_duration = reduce(lambda x, y: x + y, self.frame_durations) / len(self.frame_durations)

        print(self.terminal.clear + 'Rotor!\n')
        print('  Direction:', 'clockwise' if self.raspberry.get_direction() == 1 else 'counterclockwise')
        print('  Angle:', self.raspberry.get_angle())
        print('  Step:', self.raspberry.get_step())
        print('  Rotations per second:')
        print('    Step sensor:')
        print('    Rotation sensor:')

        print('Frames per second: ', round(1000 / average_duration, 2))

        print('WebSockets:')
        print('  Connections:', self.web_client.get_connection_count())
        print('  Last message:', self.last_message)

        print('Current program:')
        print('  ', self.graphics.get_program(), self.graphics.get_parameter())

        print('Effects:')
        print('  ', self.graphics.get_effects())

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
        leds = self.graphics.calculate(angle)
        self.raspberry.update_leds(leds)

def main():
    rotor = Rotor(30)
    rotor.start()

if __name__ == '__main__':
    main()
