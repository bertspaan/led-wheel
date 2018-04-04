class Controls:

    max = 127
    mid_threshold = 16

    pad_mapping = {
        0: 'walk_left_right',
        1: 'sine_wave',
        2: 'front'
    }

    knob_mapping = {
        0: (['effect', 'strobe'], 'zero_to_one'),
        1: (['animation_direction', 'strobe'], 'minus_one_to_one')
    }

    def map_pad(self, id):
        if id in self.pad_mapping:
            return self.pad_mapping[id]
        else:
            return None

    def map_knob(self, id, value):
        v1 = round(self.zero_to_one(value), 3)
        v2 = round(self.minus_one_to_one(value), 3)
        # print(id, value, v1, v2)

        return (0, 0)

    def zero_to_one(self, value):
        return value / self.max

    def minus_one_to_one(self, value):
        if abs(self.max / 2 - value) < self.mid_threshold:
            return 0.5
        elif value <= self.max / 2 - self.mid_threshold:
            return value / (self.max / 2 - self.mid_threshold) * 0.5
        elif value >= self.max / 2 + self.mid_threshold:
            return (value - self.max / 2 - self.mid_threshold) / (self.max / 2 - self.mid_threshold) * 0.5 + 0.5
