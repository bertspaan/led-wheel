import math

def single_light(angle, tick, parameter):
    return 1

 # (ledCount, wheelAngle, ledAngle, beat, parameter) {
# var diff = Math.abs(wheelAngle - ledAngle)
# if (diff < (360 / (ledCount * 2))) {
# return 1
# }

def front(angle, tick, parameter):
    if angle < 30:
        return 1
    else:
        return 0

def sine_wave(angle, tick, parameter):
    return (math.sin(math.radians(angle)) + 1) / 2

def walk_left_right(angle, tick, parameter):
    x = (math.sin(math.radians(angle)) + 1) / 2
    mx = (x + tick / 1000) % 1

    if mx >= 0 and mx < 0.5:
        return 1
    else:
        return 0


def fade_left_right(angle, tick, parameter):
    return 0

programs = {
    'single_light': single_light,
    'front': front,
    'sine_wave': sine_wave,
    'walk_left_right': walk_left_right
}

# lambda x: x * 2 + 10

# var patterns = {
# 'Single light': function (ledCount, wheelAngle, ledAngle, beat, parameter) {
# var diff = Math.abs(wheelAngle - ledAngle)
# if (diff < (360 / (ledCount * 2))) {
# return 1
# }
# },
# 'Front': function (ledCount, wheelAngle, ledAngle, beat, parameter) {
# var diff = Math.abs(ledAngle - 180)
# var width = 360 / ledCount * parameter * 8
#
# if (diff < width) {
# return 1
# } else if (diff < width * 2) {
# return -(diff - width) / (width * 2) + 1
# }
# },
# 'Sine wave': function (ledCount, wheelAngle, ledAngle, beat, parameter) {
# var period = Math.round(parameter * 10)
# return (Math.sin(toRad((ledAngle - 45) * period)) + 1) / 2
# },
# 'Alternating': function (ledCount, wheelAngle, ledAngle, beat, parameter) {
# var buckets = Math.max(1, Math.round(parameter * ledCount) * 2)
# var bucketSize = 360 / buckets
# var times = Math.floor(ledAngle / bucketSize)
# return 1 - ((times + (beat % 2)) % 2)
# }
# }
