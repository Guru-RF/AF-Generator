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

audio = audiobusio.I2SOut(board.GP27, board.GP28, board.GP26)

wave_file = open("StreetChicken.wav", "rb")
wav = audiocore.WaveFile(wave_file)

while True:
	print("Playing wav file!")
	audio.play(wav)

	while audio.playing:
	    pass

	print("Done!")


