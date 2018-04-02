#!/usr/bin/env python3

import Adafruit_PCA9685

pwms = [
  Adafruit_PCA9685.PCA9685(0x40),
  Adafruit_PCA9685.PCA9685(0x41)
]

for pwm in pwms:
  for i in range(16):
    pwm.set_pwm(i, 0, 0)
