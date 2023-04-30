# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This test will initialize the display using displayio and draw a solid green
background, a smaller purple rectangle, and some yellow text.
"""

import time
import array
import math
import audiocore
import audiobusio
import board
import terminalio
import displayio
import busio
from adafruit_display_text import label
from adafruit_ssd1351 import SSD1351


audio = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)

wave_file = open("StreetChicken.wav", "rb")
wav = audiocore.WaveFile(wave_file)


# Release any resources currently in use for the displays
displayio.release_displays()

spi = busio.SPI(board.GP18, board.GP19, board.GP16)

tft_cs = board.GP20
tft_dc = board.GP21

#display_bus = displayio.FourWire(
#    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP22, baudrate=16000000
#)

display_bus = displayio.FourWire(
    spi, command=tft_dc, chip_select=tft_cs, reset=board.GP22, baudrate=5000000
)

display = SSD1351(display_bus, width=128, height=128)

## Make the display context
splash = displayio.Group()
display.show(splash)

color_bitmap = displayio.Bitmap(128, 128, 1)
color_palette = displayio.Palette(1)
color_palette[0] = 0x00FF00  # Bright Green

bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
splash.append(bg_sprite)


## Draw a label
text = "RF.Guru!"
text_area = label.Label(terminalio.FONT, text=text, color=0x000000, x=30, y=64)
splash.append(text_area)


while True:
	print("Playing wav file!")
	audio.play(wav)

	while audio.playing:
	    pass

	print("Done!")


