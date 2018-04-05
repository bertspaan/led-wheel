class Controls:

    max = 127
    mid_threshold = 8

    pad_mapping = {
        2: 'fan',
        3: 'random'
    }

    knob_mapping = {
        0: ('effect', 'strobe', 'zero_to_one'),
        1: ('effect', 'dim', 'zero_to_one'),
        2: ('ceiling_led', None, 'zero_to_one'),

        4: ('effect', 'blur', 'zero_to_one'),

        6: ('animation_rps', None, 'minus_one_to_one'),
        7: ('parameter', None, 'zero_to_one')
    }

    def __init__(self):
        self.map_value_funcs = {
            'zero_to_one': self.zero_to_one,
            'minus_one_to_one': self.minus_one_to_one
        }

    def map_pad(self, id):
        if id in self.pad_mapping:
            return self.pad_mapping[id]
        else:
            return None

    def map_knob(self, id, value):
        if id in self.knob_mapping:
            mapping = self.knob_mapping[id]
            map_value_func = self.map_value_funcs[mapping[2]]
            mapped_value = map_value_func(value)
            return (mapping[0], mapping[1], mapped_value)
        else:
            return None

    def zero_to_one(self, value):
        return value / self.max

    def minus_one_to_one(self, value):
        if abs(self.max / 2 - value) < self.mid_threshold:
            return 0
        elif value <= self.max / 2 - self.mid_threshold:
            return (1 - (value / (self.max / 2 - self.mid_threshold))) * -1
        elif value >= self.max / 2 + self.mid_threshold:
            return (value - self.max / 2 - self.mid_threshold) / (self.max / 2 - self.mid_threshold)
