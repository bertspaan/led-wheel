import time
from threading import Thread
from signal import pause
from collections import deque
from functools import reduce

io_available = False

try:
    from gpiozero import LightSensor
    io_available = True
except ModuleNotFoundError:
    print("gpiozero not found, continuing regardless!")
except RuntimeError:
    print("Error importing gpiozero! This is probably because you need superuser privileges!")

class GPIO:

    step_count = 6

    pin_step = 20
    pin_rotation = 21

    last_step = 0
    last_rotation = 0
    last_steps = deque([], step_count)

    def diffs(self, iterable):
        it = iter(iterable)
        a = next(it, None)

        for b in it:
            yield a - b
            a = b

    def get_ms(self):
        return time.time() * 1000.0

    def step(self):
        ms = self.get_ms()
        self.last_steps.appendleft(ms)

        if len(self.last_steps) >= 2:
            average = reduce(lambda x, y: x + y, self.diffs(self.last_steps)) / len(self.last_steps)
            print("Step RPM:", round(1000 / (average * self.step_count), 2))

    def rotation(self):
        ms = self.get_ms()

        print("Rotation RPM:", round(1000 / (ms - self.last_rotation), 2))

        self.last_rotation = ms

    def run(self):
        sensor_step = LightSensor(self.pin_step)
        sensor_step.when_dark = self.step

        # sensor_rotation = MotionSensor(self.pin_rotation)
        # sensor_rotation.when_motion = self.rotation

        # while True:
        #     print(sensor_rotation.value)
        #     time.sleep(0.1)

        pause()

    def start(self):
        if not io_available:
            return

        print("Starting GPIO!")
        thread = Thread(target=self.run)
        thread.start()
