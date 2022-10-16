# Write to the Pimoroni pico display
# Author: Eric Ayers <ericzundel@gmail.com>

import board
import displayio
import terminalio

# 3rd Party imports
from adafruit_display_text import label
import adafruit_st7789

class screen:
    # spi - instance of the spi module already initialized
    def __init__(self, spi, **kwargs):
        print("Raspberry Pi Pico/CircuitPython ST7789 SPI IPS Display")
        print(adafruit_st7789.__name__ + " version: " + adafruit_st7789.__version__)

        tft_cs = board.GP17
        tft_dc = board.GP16
        display_bus = displayio.FourWire(spi, command=tft_dc, chip_select=tft_cs)
        self.display = adafruit_st7789.ST7789(
            display_bus, width=135, height=240, rowstart=40, colstart=53
        )


    def paint_screen(self, bgcolor=0x0000FF):
        self.display.rotation = 180
        # Make the display context
        splash = displayio.Group()
        self.display.show(splash)

        color_bitmap = displayio.Bitmap(135, 240, 1)
        color_palette = displayio.Palette(1)
        color_palette[0] = 0x00FF00

        bg_sprite = displayio.TileGrid(
            color_bitmap, pixel_shader=color_palette, x=0, y=0
        )
        splash.append(bg_sprite)

        # Draw a smaller inner rectangle
        inner_bitmap = displayio.Bitmap(133, 238, 1)
        inner_palette = displayio.Palette(1)
        inner_palette[0] = bgcolor
        inner_sprite = displayio.TileGrid(
            inner_bitmap, pixel_shader=inner_palette, x=1, y=1
        )
        splash.append(inner_sprite)

        # Draw a label
        text_group1 = displayio.Group(scale=1, x=20, y=40)
        text1 = "wildestpixel"
        text_area1 = label.Label(terminalio.FONT, text=text1, color=0xFF0000)
        text_group1.append(text_area1)  # Subgroup for text scaling
        # Draw a label
        text_group2 = displayio.Group(scale=1, x=20, y=60)
        text2 = "CircuitPython"
        text_area2 = label.Label(terminalio.FONT, text=text2, color=0xFFFFFF)
        text_group2.append(text_area2)  # Subgroup for text scaling

        # Draw a label
        text_group3 = displayio.Group(scale=1, x=20, y=100)
        text3 = adafruit_st7789.__name__
        text_area3 = label.Label(terminalio.FONT, text=text3, color=0x0000000)
        text_group3.append(text_area3)  # Subgroup for text scaling
        # Draw a label
        text_group4 = displayio.Group(scale=2, x=20, y=120)
        text4 = adafruit_st7789.__version__
        text_area4 = label.Label(terminalio.FONT, text=text4, color=0x000000)
        text_group4.append(text_area4)  # Subgroup for text scaling

        splash.append(text_group1)
        splash.append(text_group2)
        splash.append(text_group3)
        splash.append(text_group4)
