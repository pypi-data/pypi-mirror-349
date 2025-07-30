Introduction
============

.. image:: https://img.shields.io/discord/327254708534116352.svg
    :target: https://adafru.it/discord
    :alt: Discord


.. image:: https://github.com/clickonben/CircuitPython_pixel_mapper/workflows/Build%20CI/badge.svg
    :target: https://github.com/clickonben/CircuitPython_pixel_mapper/actions
    :alt: Build Status


.. image:: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json
    :target: https://github.com/astral-sh/ruff
    :alt: Code Style: Ruff

Pixel Mapper for Adafruit_CircuitPython_LED_Animation
===============================================================

This library provides custom pixel mappers for use with the Adafruit CircuitPython LED Animation library.

The built-in mappers only support arranging multiple matrices in the direction the internal LED strip is physically wired. This library extends that functionality by allowing you to stack panels vertically or horizontally, regardless of wiring direction.

You can also apply optional x and y offsets, making it easier to treat sections of a larger matrix as independent regions — without manually defining complex pixel maps.

Key Features
============
Combine multiple LED panels into vertical or horizontal matrix layouts

Support for snaking layouts (e.g. zigzag wiring patterns)

Optional x/y offsets for sub-matrix mapping

Compatible with Adafruit's CircuitPython LED Animation library

Dependencies
=============
This driver depends on:

* `Adafruit CircuitPython <https://github.com/adafruit/circuitpython>`_

Please ensure all dependencies are available on the CircuitPython filesystem.
This is easily achieved by downloading
`the Adafruit library and driver bundle <https://circuitpython.org/libraries>`_
or individual libraries can be installed using
`circup <https://github.com/adafruit/circup>`_.

Installing from PyPI
=====================

On supported GNU/Linux systems like the Raspberry Pi, you can install the driver locally `from
PyPI <https://pypi.org/project/circuitpython-pixel-mapper/>`_.
To install for current user:

.. code-block:: shell

    pip3 install circuitpython-pixel-mapper

To install system-wide (this may be required in some cases):

.. code-block:: shell

    sudo pip3 install circuitpython-pixel-mapper

To install in a virtual environment in your current project:

.. code-block:: shell

    mkdir project-name && cd project-name
    python3 -m venv .venv
    source .env/bin/activate
    pip3 install circuitpython-pixel-mapper

Installing to a Connected CircuitPython Device with Circup
==========================================================

Make sure that you have ``circup`` installed in your Python environment.
Install it with the following command if necessary:

.. code-block:: shell

    pip3 install circup

With ``circup`` installed and your CircuitPython device connected use the
following command to install:

.. code-block:: shell

    circup install pixel_mapper

Or the following command to update an existing version:

.. code-block:: shell

    circup update

Usage Example
=============

.. code:: python

    import board
    import neopixel

    from adafruit_led_animation import helper
    from adafruit_led_animation.animation.chase import Chase
    from adafruit_led_animation.animation.comet import Comet
    from adafruit_led_animation.animation.rainbowchase import RainbowChase
    from adafruit_led_animation.animation.rainbowcomet import RainbowComet
    from adafruit_led_animation.color import AMBER, JADE, PURPLE, RED, GREEN, BLUE,OLD_LACE,ORANGE
    from imports.pixel_mappers import vertical_stacked_panels_mapper

    # Update to match the pin connected to your NeoPixels
    pixel_pin = board.GP2
    # Update to match the number of NeoPixels you have connected
    pixel_num = 1024

    pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.75, auto_write=False)
    pixels.fill((0, 0, 0))

    pixel_wing_top_left = helper.PixelMap.horizontal_lines(
        pixels,
        16,
        16,
        vertical_stacked_panels_mapper(32, 32, panel_height=8, reverse=True, x_offset=16, y_offset=16),
    )

    pixel_wing_botom_left = helper.PixelMap.horizontal_lines(
        pixels,
        16,
        16,
        vertical_stacked_panels_mapper(32, 32, panel_height=8, reverse=True, x_offset=16)
    )

    pixel_wing_top_right = helper.PixelMap.horizontal_lines(
        pixels,
        16,
        16,
        vertical_stacked_panels_mapper(32, 32, panel_height=8, reverse=True, y_offset=16),
    )

    pixel_wing_botom_right = helper.PixelMap.horizontal_lines(
        pixels,
        16,
        16,
        vertical_stacked_panels_mapper(32, 32, panel_height=8, reverse=True)
    )

    comet = Comet(pixel_wing_top_left, speed=0.1, color=AMBER, tail_length=6, bounce=True)
    chase = Chase(pixel_wing_botom_left, speed=0.1, size=3, spacing=6, color=JADE)
    rainbow_chase = RainbowChase(pixel_wing_top_right, speed=0.1, size=3, spacing=2, step=8)
    rainbow_comet = RainbowComet(pixel_wing_botom_right, speed=0.05, tail_length=7, bounce=True)

    while True:
        comet.animate()
        chase.animate()
        rainbow_chase.animate()
        rainbow_comet.animate()



Documentation
=============
API documentation for this library can be found on `Read the Docs <https://circuitpython-pixel-mapper.readthedocs.io/>`_.

For information on building library documentation, please check out
`this guide <https://learn.adafruit.com/creating-and-sharing-a-circuitpython-library/sharing-our-docs-on-readthedocs#sphinx-5-1>`_.

Contributing
============

Contributions are welcome! Please read our `Code of Conduct
<https://github.com/clickonben/CircuitPython_pixel_mapper/blob/HEAD/CODE_OF_CONDUCT.md>`_
before contributing to help this project stay welcoming.
