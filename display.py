# SPDX-FileCopyrightText: 2018 Dave Astels for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
Display code for signal generator.

Adafruit invests time and resources providing this open source code.
Please support Adafruit and open source hardware by purchasing
products from Adafruit!

Written by Dave Astels for Adafruit Industries
Copyright (c) 2018 Adafruit Industries
Licensed under the MIT license.

All text above must be included in any redistribution.
"""

import math
import board
import busio
import shapes
import displayio
import digitalio
from adafruit_ssd1351 import SSD1351

# Display stuff
# Release any resources currently in use for the displays
displayio.release_displays()


class Display:
    """Manage the OLED Featherwing display"""


    spi = None
    oled = None
    shape = None
    frequency = None

    def __init__(self):
        self.spi = busio.SPI(board.GP18, board.GP19, board.GP16)
        tft_cs = board.GP20
        tft_dc = board.GP21

        display_bus = displayio.FourWire(
            self.spi, command=tft_dc, chip_select=tft_cs, reset=board.GP22, baudrate=5000000
        )
        self.oled = SSD1351(display_bus, width=128, height=128)

        self.oled.fill(0)
        self.oled.show()


    def draw_sine(self):
        for i in range(32):
            self.oled.pixel(i, int(math.sin(i/32 * math.pi * 2) * 16) + 16, 1)


    def draw_square(self):
        for i in range(16):
            self.oled.pixel(0, 32 - i, 1)
            self.oled.pixel(i, 31, 1)
            self.oled.pixel(31, i, 1)
            self.oled.pixel(15, 16 + i, 1)
            self.oled.pixel(15, i, 1)
            self.oled.pixel(16 + i, 0, 1)


    def draw_triangle(self):
        for i in range(8):
            self.oled.pixel(i, 16 + i * 2, 1)
            self.oled.pixel(8 + i, 32 - i * 2, 1)
            self.oled.pixel(16 + i, 16 - i * 2, 1)
            self.oled.pixel(24 + i, i * 2, 1)


    def draw_sawtooth(self):
        for i in range(16):
            self.oled.pixel(0, 16 + i, 1)
            self.oled.pixel(31, i, 1)
        for i in range(32):
            self.oled.pixel(i, 31 - i, 1)


    def update(self):
        self.oled.fill(0)
        if self.shape == shapes.SINE:
            self.draw_sine()
        elif self.shape == shapes.SQUARE:
            self.draw_square()
        elif self.shape == shapes.TRIANGLE:
            self.draw_triangle()
        elif self.shape == shapes.SAWTOOTH:
            self.draw_sawtooth()
        self.oled.text("{0}".format(self.frequency), 40, 10, 1)
        self.oled.show()


    def update_shape(self, shape):
        if shape != self.shape:
            self.shape = shape
            self.update()


    def update_frequency(self, frequency):
        if frequency != self.frequency:
            self.frequency = frequency
            self.update()
