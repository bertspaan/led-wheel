from pygame import midi

def init_lpd8():
    """
    Connect to the midi controller and open a device handle.
    """
    midi.init()

    device = None
    for i in range(midi.get_count()):
        # Device info is returned as a tuple in the form:
        #    (interf, name, input, output, opened)
        info = midi.get_device_info(i)
        _logger.debug('Device %s: %s', i, info)

        # print(info[1].decode("utf-8"))
        if 'LPD8' in info[1].decode("utf-8") and info[2] == 1:
            device = midi.Input(i)
            _logger.info('Connected to device: %s', info)
            atexit.register(device.close)

    if not device:
        raise RuntimeError('LPD8 MIDI device not found')

    return device
#
#
# def init_hue(hue_ip):
#     """
#     Connect to the philips hue bridge. The first time that a connection is
#     made, you will need to press the button on the Philips bridge to generate
#     user credentials. Credentials are then stored in the home directory for
#     future sessions.
#     """
#     bridge = phue.Bridge(hue_ip)
#     _logger.debug(bridge.get_api())
#
#     for i, light in enumerate(bridge.lights, start=1):
#         light.on = True
#         _logger.info('Found light %s: %s', i, light.name)
#
#     for i, group in enumerate(bridge.groups, start=1):
#         _logger.info('Found group %s: %s', i, group.name)
#
#     return bridge
#
#
class MidiController(object):

    def __init__(self, device):

        self.device = device
        self.update_pad_flag = False


    def loop_forever(self):
        """
        Loop and watch for MIDI events.

        Akai LPD8 midi controller codes:

            Each message is encoded as [status, data1, data2, data3]

            Mode PAD   : controller will send MIDI notes
            Mode CHNG  : controller will send Program Change
            Mode CC    : controller will send MIDI Control Change

                           Program #   Pad/Knob #  Intensity  N/A
                           ---------   ----------  ---------  ---
            Knobs          176-179     1-8         0-127      0
            CC Hit         176-179     1-6/8-9     0-127      0
            CC Release     176-179     1-6/8-9     0          0
            PAD Hit        144-147     36-43       0-127      0
            PAD Release    128-131     36-43       127        0
            CHNG Hit       192-195     0-7         0          0
            CHNG Release   -           -           -          -
        """
        while True:
            while self.device.poll():
                event, timestamp = self.device.read(1)[0]
                _logger.debug(event)

                print(event)

                # if 176 <= event[0] <= 179:
                #     self.knob(event[1], event[2])
                #
                # elif 144 <= event[0] <= 147:
                #     self.pad_hit(event[0] - 143, event[1])
                #
                # elif 128 <= event[0] <= 131:
                #     self.pad_release(event[0] - 127, event[1])
                #
                # elif 192 <= event[0] <= 195:
                #     self.pad_prog_chng(event[1])

            time.sleep(0.01)
