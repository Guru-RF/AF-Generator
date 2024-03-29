# SPDX-FileCopyrightText: 2018 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Outpout generator code for signal generator.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import math
import array
import board
#import audioio
import audiocore
import audiocore
import audiobusio
import shapes


def length(frequency):
    return int(32000 / frequency)



class Generator:

    sample = None
    dac = None
    shape = None
    frequency = None


    def __init__(self):
        self.dac = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)
        #self.dac = audioio.AudioOut(board.A0)

    def reallocate(self, frequency):
        self.sample = array.array("h", [0] * length(frequency))


    def make_sine(self):
        l = len(self.sample)
	tone_volume = 0.4 # 0.1
        for i in range(l):
            self.sample[i] = min(2 ** 15 - 1, int(math.sin(math.pi * 2 * i / l) * (2 ** 15)))
	    #self.sample[i] = int((1 + math.sin(math.pi * 2 * i / l)) * tone_volume * (2 ** 15 - 1))


    def make_square(self):
        l = len(self.sample)
        half_l = l // 2
        for i in range(l):
            if i < half_l:
                self.sample[i] = -1 * ((2 ** 15) - 1)
            else:
                self.sample[i] = (2 ** 15) - 1


    def make_triangle(self):
        l = len(self.sample)
        half_l = l // 2
        s = 0
        for i in range(l):
            if i <= half_l:
                s = int((i / half_l) * (2 ** 16)) - (2 ** 15)
            else:
                s = int((1 - ((i - half_l) / half_l)) * (2 ** 16)) - (2 ** 15)
            self.sample[i] = min(2 ** 15 -1, s)



    def make_sawtooth(self):
        l = len(self.sample)
        for i in range(l):
            self.sample[i] = int((i / l) * (2 ** 16)) - (2 ** 15)


    def update(self, shape, frequency):
        if shape == self.shape and frequency == self.frequency:
            return

        if frequency != self.frequency:
            self.reallocate(frequency)
            self.frequency = frequency

        self.shape = shape
        if shape == shapes.SINE:
            self.make_sine()
        elif shape == shapes.SQUARE:
            self.make_square()
        elif shape == shapes.TRIANGLE:
            self.make_triangle()
        elif shape == shapes.SAWTOOTH:
            self.make_sawtooth()

        self.dac.stop()
        self.dac.play(audiocore.RawSample(self.sample, channel_count=2, sample_rate=64000), loop=True)
