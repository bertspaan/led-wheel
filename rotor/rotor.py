#!/usr/bin/env python3

import os
import json
import atexit
import click
import logging
import time
from collections import deque
from functools import reduce

from devices.raspberry import Raspberry
from devices.web_client import WebClient

from graphics import Graphics

logger = logging.getLogger('rotor')

class Rotor:

    frame_durations = deque([], 20)
    fps = 60

    def __init__(self, led_count):
        self.graphics = Graphics(led_count)

        self.raspberry = Raspberry()
        self.web_client = WebClient()

    def start(self):
        self.raspberry.start()
        self.web_client.start()

        frame = 0
        last = time.perf_counter()

        frame_ms = 1000 / self.fps

        while True:
            self.update()
            frame += 1

            current = time.perf_counter()
            passed = (current - last) * 1000

            self.frame_durations.appendleft(passed)

            if frame % (self.fps * 5) == 0:
                average = reduce(lambda x, y: x + y, self.frame_durations) / len(self.frame_durations)
                print (round(1000 / average, 2), 'FPS')

            if frame_ms - passed > 0:
                time.sleep((frame_ms - passed) / 1000)

            last = current

    def update(self):
        angle = self.raspberry.get_angle()
        leds = self.graphics.calculate(angle)
        self.raspberry.update_leds(leds)

@click.command()
@click.option('--debug/--no-debug', default=False, help='Enable verbose logging.')
def main(debug):

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    rotor = Rotor(30)
    rotor.start()

if __name__ == '__main__':
    main()
