from scipy.ndimage.filters import gaussian_filter

def blur(leds, parameter, tick):
    blurred = gaussian_filter(leds, sigma=parameter * 3, mode='wrap')
    return [float(led) for led in blurred]

def strobe(leds, parameter, tick):
    return leds

def dim(leds, parameter, tick):
    return [led * (1 - parameter) for led in leds]

effects = {
    'blur': blur,
    'strobe': strobe,
    'dim': dim
}
