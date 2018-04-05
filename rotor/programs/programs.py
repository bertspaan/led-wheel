import math
import random

# p1: fixed angle light 0
# p2: fixed angle light 0 + 15
# p3: fixed angle light elke drie
# p4: fixed angle light: eerste helft
# p5: 10, 20, 30 -> 5, 15, 25
# p6: 1-10, 11-20, 21-30
# p7: waaier
# p8: random beams
def in_angle_range(mid_angle, threshold, led_angle):
    if abs((mid_angle - (led_angle + 360)) % 360) <= threshold:
        return 1
    else:
        return 0

# def fixed_0(angle, tick, parameter):
#     if 180 - abs(180 - angle) < (180 * parameter):
#         return 1
#     else:
#         return 0

# def fixed_0_180
#
#
# def left_right

def fan(angle, tick, parameter):
    x = (math.sin(math.radians(angle)) + 1) / 2
    mx = (x + tick / 1000) % 2

    if mx >= 0 and mx < 1:
        return 1
    else:
        return 0

def random_beams(angle, tick, parameter):
    random.seed(tick)
    random_angle = random.randint(0, 359)
    return in_angle_range(random_angle, 60 * parameter, angle)

programs = {
    'fan': fan,
    'random_beams': random_beams
}
