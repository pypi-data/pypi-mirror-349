# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Ben Robinson for CodingFlow
#
# SPDX-License-Identifier: Unlicense
import board
import neopixel
from adafruit_led_animation import helper
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.color import AMBER, JADE
from imports.pixel_mappers import vertical_stacked_panels_mapper

# This example is for a 32x32 matrix made from four 8x32 panels stacked vertically.
# Each panel uses a snaking (zigzag) layout: columns alternate direction.
#
# The matrix is logically split into four 16x16 quadrants:
# - top_left
# - top_right
# - bottom_left
# - bottom_right
#
# The (0,0) origin is at the top-left corner of the matrix.

# Update to match the pin connected to your NeoPixels
pixel_pin = board.GP2

# Total number of pixels: 4 panels * 8 rows * 32 columns = 1024
pixel_num = 1024

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.75, auto_write=False)
pixels.fill((0, 0, 0))

pixel_wing_bottom_right = helper.PixelMap.horizontal_lines(
    pixels,
    16,
    16,
    vertical_stacked_panels_mapper(32, 32, panel_height=8, x_offset=16, y_offset=16),
)

pixel_wing_top_right = helper.PixelMap.horizontal_lines(
    pixels, 16, 16, vertical_stacked_panels_mapper(32, 32, panel_height=8, x_offset=16)
)

pixel_wing_bottom_left = helper.PixelMap.horizontal_lines(
    pixels,
    16,
    16,
    vertical_stacked_panels_mapper(32, 32, panel_height=8, y_offset=16),
)

pixel_wing_top_left = helper.PixelMap.horizontal_lines(
    pixels,
    16,
    16,
    vertical_stacked_panels_mapper(32, 32, panel_height=8),
)

# Create animations for each quadrant
comet = Comet(pixel_wing_top_left, speed=0.1, color=AMBER, tail_length=6, bounce=True)
chase = Chase(pixel_wing_bottom_left, speed=0.1, size=3, spacing=6, color=JADE)
rainbow_chase = RainbowChase(pixel_wing_top_right, speed=0.1, size=3, spacing=2, step=8)
rainbow_comet = RainbowComet(pixel_wing_bottom_right, speed=0.05, tail_length=7, bounce=True)

# Run animations
while True:
    comet.animate()
    chase.animate()
    rainbow_chase.animate()
    rainbow_comet.animate()
