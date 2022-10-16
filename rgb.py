#  Control the RGB LED on the Pimoroni pico display using a Raspberry Pi Pico
# Author: Eric Ayers <ericzundel@gmail.com>

import board
import pwmio

class FakeRGB:
    def __init__(self, **kwargs):
        pass
    def set(self, r, g, b):
        pass
    def off(self):
        pass


class RGB:
    def __init__(self, **kwargs):
        self.r_out = pwmio.PWMOut(board.GP6, frequency=1000) # pin 9
        self.g_out = pwmio.PWMOut(board.GP7, frequency=1000) # pin 10
        self.b_out = pwmio.PWMOut(board.GP8, frequency=1000) # pin 11

    # Input  range from 0 to 255
    def set(self, r, g, b):
        self.r_out.duty_cycle = r << 8
        self.g_out.duty_cycle = g << 8
        self.b_out.duty_cycle = b << 8


    def off(self):
        self.r_out.duty_cycle = 0xffff
        self.g_out.duty_cycle = 0xffff
        self.b_out.duty_cycle = 0xffff

