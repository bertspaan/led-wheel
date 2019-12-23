import math
from scipy.ndimage.filters import gaussian_filter

def blur(leds, parameter, beat, ms):
    blurred = gaussian_filter(leds, sigma=parameter * 3, mode='wrap')
    return [float(led) for led in blurred]

def mix(led, last_led, parameter):
    if led < last_led:
        return (last_led - led) * parameter + led
    else:
        return led

last_leds = None
def motion_blur(leds, parameter, beat, ms):
    p_min = 0.8
    p_max = 0.995

    global last_leds

    if last_leds is None:
        last_leds = leds[:]

    p = 0
    if parameter > 0:
        p = p_min + parameter * (p_max - p_min)

    leds = [mix(leds[i], last_leds[i], p) for i in range(len(leds))]
    last_leds = leds[:]

    return leds

def strobe(leds, parameter, beat, ms):
    tick = round((ms / 20.1) % 64)
    if parameter == 0:
        return leds
    return[led if ((tick / math.pow(2, round((1 - parameter) * 6))) % 2 == 0) else 0 for led in leds]

def dim(leds, parameter, beat, ms):
    return [led * parameter for led in leds]

effects = {
    'blur': blur,
    'motion_blur': motion_blur,
    'strobe': strobe,
    'dim': dim
}
