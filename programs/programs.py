import math
import random


# TODO:
# waaier op ongeanimeerde angle
# toevoegen nulhoekijkpunt
# time on !!!
# versnelling/vertraging

def in_angle_range(mid_angle, threshold, led_angle):
    if abs((led_angle + 180) % 360 - (mid_angle + 180) % 360) < threshold:
        return 1
    else:
        return 0

def fixed_one(angle, beat, parameter):
    return in_angle_range(0, 12 + 348 * parameter, angle)

def fixed_two(angle, beat, parameter):
    return in_angle_range(0, 12 + 168 * parameter, angle % 180)

def fixed_half(angle, beat, parameter):
    return in_angle_range(90, 90 + 180 * parameter, angle)

def fixed_one_fifth(angle, beat, parameter):
    return in_angle_range(0, 12 + 60 * parameter, angle % 72)

# def left_right(angle, beat, parameter):
#     position = beat % 2
#     return (1 - position) if angle < 180 else position
#
# def walk_six(angle, beat, parameter):
#     return in_angle_range(60 * (beat % 2), 12 + parameter * 48, angle % 120)
#
# def walk_thirds(angle, beat, parameter):
#     return in_angle_range(120 * (beat % 3), 60 + parameter * 120, angle)
#
# def walk_one_fifth(angle, beat, parameter):
#     return in_angle_range(24 * (beat % 3), 12 + 60 * parameter, angle % 72)
#
# def fan(angle, beat, parameter):
#     x = (math.sin(math.radians(angle)) + 1) / 2
#     mx = (x + beat / 5) % 2
#
#     if mx >= 0 and mx < 1:
#         return 1
#     else:
#         return 0
#
# def random_beams(angle, beat, parameter):
#     random.seed(beat)
#     random_angle = random.randint(0, 359)
#     return in_angle_range(random_angle, 12 + 168 * parameter, angle)

programs = {
    'fixed_one': fixed_one,
    'fixed_two': fixed_two,
    'fixed_one_fifth': fixed_one_fifth,
    'fixed_half': fixed_half,
    # 'walk_one_fifth': walk_one_fifth,
    # 'walk_thirds': walk_thirds
    # 'left_right': left_right,
    # 'fan': fan,
    # 'random_beams': random_beams
}
