#!/usr/bin/env python3

import os
import json
import atexit
import click
import logging
import time

from devices.raspberry import Device
from graphics import Graphics

logger = logging.getLogger('rotor')
graphics = Graphics(30)

device = Device()
device.start()

fps = 60

# Functions:
#  - GPIO interupts for rotation speed
#  - Read MIDI
#  - Rotation
#  - Compute + mix programs
#  - Set LEDs

def tick(fps, callback):
    frame = 0
    start = time.perf_counter()
    while True:
        callback()
        frame += 1
        target = frame / fps
        passed = time.perf_counter() - start
        differ = target - passed
        if differ > 0:
            time.sleep(differ)

def update():

    angle = Device.get_angle()

    leds = graphics.calculate(angle)


    device.update_leds(leds)
    # ledCount,  parameters


        #
        #
        #
        #     # reken uit alle programma's + effecten
        #     # resultaat is byte array
        #     # stuur naar display
        #
        #     # average_time_between_frame_start_and_write!
        #
        #     # reken uit hoe lang-ie echt moet slapen
        #     time.sleep(1 / fps)
    # print("vissen")

    # var animationMsPerDegree = 1000 / (animationRps * 360)
    # animationAngle = (animationAngle + (timestamp - lastAnimationAngleTimestamp) * (1 / animationMsPerDegree)) % 360
    # lastAnimationAngleTimestamp = timestamp
    #
    # for (var index = 0; index < ledCount; index++) {
    # var ledAngle = wheelAngle + (360 / ledCount) * index
    # if (!lockRps) {
    #  ledAngle += animationAngle
    # }
    # ledAngle = ledAngle % 360
    # setLight(index, ledCount, wheelAngle, ledAngle, beat, parameter)
    # }
    #
    # window.requestAnimationFrame(animate)
    # }


@click.command()
@click.option('--debug/--no-debug', default=False, help='Enable verbose logging.')
def main(debug):

    if debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    tick(fps, update)

if __name__ == '__main__':
    main()
