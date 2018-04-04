import time
from threading import Thread
from signal import pause
from collections import deque
from functools import reduce

io_available = False

try:
    from gpiozero import LightSensor, InputDevice, SmoothedInputDevice, Button
    io_available = True
except ModuleNotFoundError:
    print("gpiozero not found, continuing regardless!")
except RuntimeError:
    print("Error importing gpiozero! This is probably because you need superuser privileges!")

class GPIO:

    direction = 1

    current_step = 0
    last_step_ms = 0
    last_angle = 0
    rps = 0

    step_count = 8

    pin_step = 21
    pin_rotation = 20

    last_step = 0
    last_rotation = 0
    last_steps = deque([], step_count)

    def __init__(self, on_step):
        self.on_step = on_step

    def diffs(self, iterable):
        it = iter(iterable)
        a = next(it, None)

        for b in it:
            yield a - b
            a = b

    def get_ms(self):
        return time.time() * 1000.0

    def on_step(self):
        ms = self.get_ms()
        self.last_steps.appendleft(ms)
        self.current_step = (self.current_step + self.direction) % self.step_count
        self.last_step_ms = ms

        if len(self.last_steps) >= 2:
            average = reduce(lambda x, y: x + y, self.diffs(self.last_steps)) / len(self.last_steps)
            self.rps = 1000 / (average * self.step_count)
            # print("Step RPS:", round(1000 / (average * self.step_count), 3))

        # on_step

    def on_rotation(self):
        ms = self.get_ms()
        # self.current_step = 0

        # print("Rotation RPS:", round(1000 / (ms - self.last_rotation), 3))

        self.last_rotation = ms


    def set_direction(self, direction):
        self.direction = direction

    def get_direction(self):
        return self.direction

    def get_angle(self):
        ms = self.get_ms()
        ms_since = ms - self.last_step_ms

        if ms_since > 3000:
            return self.last_angle

        last_step_angle = 360 / self.step_count * self.current_step
        angle_since = ms_since / 1000 * self.rps * 360

        self.last_angle = last_step_angle + angle_since
        return self.last_angle

    def get_step(self):
        return self.current_step

    def run(self):
        sensor_step = Button(self.pin_step, pull_up=True)
        sensor_step.when_pressed = self.on_step

        sensor_rotation = Button(self.pin_rotation, pull_up=True)
        sensor_rotation.when_pressed = self.on_rotation

        pause()

    def start(self):
        if not io_available:
            return

        print("Starting GPIO!")
        thread = Thread(target=self.run)
        thread.start()
