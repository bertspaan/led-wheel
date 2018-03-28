#!/usr/bin/env python3

import os
import json
import atexit
import click
import logging

from devices.raspberry import Device

logger = logging.getLogger('rotor')

# Functions:
#  - GPIO interupts for rotation speed
#  - Read MIDI
#  - Rotation
#  - Compute + mix programs
#  - Set LEDs

# function animate () {
# var timestamp = Date.now()
# var beatDurationMs = 60 * 1000 / bpm
# if (timestamp - lastBeatTimestamp >= beatDurationMs) {
# beat += 1
# lastBeatTimestamp = timestamp
# }
#
# wheelAngle = getWheelAngle()
#
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

    device = Device()
    device.start()

    # thread = LightMonitorThread(bridge)
    # thread.start()

    # device = init_lpd8()
    # controller = MidiController(device)
    #
    # try:
    #     controller.loop_forever()
    # except KeyboardInterrupt:
    #     pass
    # except Exception as e:
    #     logger.error(e)
    #
    # thread.active = False
    # thread.join()


if __name__ == "__main__":
    main()
