def blur(index, value, parameter, leds):
    return value

def strobe(index, value, parameter, leds):
    return 0

def dim(index, value, parameter, leds):
    return value * (1 - parameter)

effects = {
    'blur': blur,
    'strobe': strobe,
    'dim': dim
}
