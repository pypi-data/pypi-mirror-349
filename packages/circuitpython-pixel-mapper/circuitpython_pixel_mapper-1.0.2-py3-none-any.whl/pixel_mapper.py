# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2025 Ben Robinson for CodingFlow
#
# SPDX-License-Identifier: MIT
"""
`pixel_mapper`
================================================================================

Pixel Mapper for Adafruit_CircuitPython_LED_Animation


* Author(s): Ben Robinson

Implementation Notes
--------------------

**Hardware:**

* `Adafruit NeoPixels <https://www.adafruit.com/category/168>`_
* `Adafruit DotStars <https://www.adafruit.com/category/885>`_

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads
"""

# imports

__version__ = "v1.0.2"
__repo__ = "https://github.com/clickonben/CircuitPython_pixel_mapper.git"


def vertical_stacked_panels_mapper(  # noqa: PLR0913, PLR0917
    width, height, panel_height=8, alternating=True, reverse=False, x_offset=0, y_offset=0
):
    """
    Maps (x, y) to index in a display made of vertically stacked 32x8 panels,
    each snaking vertically up and down, with panels stacked top-to-bottom.

    :param width: Full grid width (e.g., 32)
    :param height: Full grid height (e.g., 32)
    :param panel_height: Height of each panel
    :param alternating: Whether to alternate rows up/down
    :param reverse: If True, panels are ordered bottom-to-top
    :param x_offset: Offset for x coordinate
    :param y_offset: Offset for y coordinate
    :return: mapper(x, y) function
    :raises ValueError: If x or y coordinates are out of bounds
    """
    panels_down = height // panel_height

    def mapper(x, y):
        adjusted_x = x + x_offset
        adjusted_y = y + y_offset
        if adjusted_x < 0:
            raise ValueError("x coordinate out of bounds")
        if adjusted_y < 0:
            raise ValueError("y coordinate out of bounds")
        if adjusted_x >= width:
            raise ValueError("x coordinate out of bounds")
        if adjusted_y >= height:
            raise ValueError("y coordinate out of bounds")

        panel_index = adjusted_y // panel_height
        if reverse:
            panel_index = panels_down - 1 - panel_index

        # which 8-row block we're in (top to bottom)
        local_y = adjusted_y % panel_height  # y within the panel

        if adjusted_x % 2 == 1 and alternating:
            pixel_in_panel = adjusted_x * panel_height + (panel_height - 1 - local_y)
        else:
            pixel_in_panel = adjusted_x * panel_height + local_y

        index = panel_index * (width * panel_height) + pixel_in_panel
        return index

    return mapper


def horizontal_stacked_panels_mapper(  # noqa: PLR0913, PLR0917
    width, height, panel_width=8, alternating=True, reverse=False, x_offset=0, y_offset=0
):
    """
    Maps (x, y) to index in a display made of horizontally stacked panels,
    each snaking vertically in columns, with panels laid left to right.

    :param width: Full matrix width (e.g., 32)
    :param height: Full matrix height (e.g., 16)
    :param panel_width: Width of each panel (default: 8)
    :param alternating: Whether to alternate columns up/down
    :param reverse: If True, panels are ordered right-to-left
    :param x_offset: Offset for x coordinate
    :param y_offset: Offset for y coordinate
    :return: mapper(x, y) function
    :raises ValueError: If x or y coordinates are out of bounds
    """
    panels_across = width // panel_width

    def mapper(x, y):
        adjusted_x = x + x_offset
        adjusted_y = y + y_offset
        if adjusted_x < 0:
            raise ValueError("x coordinate out of bounds")
        if adjusted_y < 0:
            raise ValueError("y coordinate out of bounds")
        if adjusted_x >= width:
            raise ValueError("x coordinate out of bounds")
        if adjusted_y >= height:
            raise ValueError("y coordinate out of bounds")

        panel_index = adjusted_x // panel_width
        if reverse:
            panel_index = panels_across - 1 - panel_index

        local_x = adjusted_x % panel_width

        if local_x % 2 == 1 and alternating:
            pixel_in_panel = local_x * height + (height - 1 - adjusted_y)
        else:
            pixel_in_panel = local_x * height + adjusted_y

        index = panel_index * (panel_width * height) + pixel_in_panel
        return index

    return mapper
