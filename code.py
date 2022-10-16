"""
adapted from http://helloraspberrypi.blogspot.com/2021/01/raspberry-pi-picocircuitpython-st7789.html
"""

# System imports
import board
import busio
from digitalio import DigitalInOut, Direction, Pull
import displayio
import os
import socketpool
import ssl
import time
import wifi

# 3rd party imports
import adafruit_requests

# Local module imports
import picodisplay
from openweather import openweather
import rgb

# returns instance of adafruit_requests module
def init_wifi(spi):
    start = time.time()
    connected = False
    savedException = 0

    print ("Prepare for flakiness!")
    for i in range(0,10):
        print("Initializing WiFi.")
        try:
            wifi.radio.connect(os.getenv('WIFI_SSID'), os.getenv('WIFI_PASSWORD'))
            connected = True
        except Exception as e:
            savedException = e
            print("Attempt: "+ str(i) +" Error Connecting: " + str(e))
            time.sleep(2)
    print ("WiFi Ready. " + str(time.time() - start) + " seconds.")

    if connected is False:
        print("Giving up and soft resetting.")
        microcontroller.reset()

    pool = socketpool.SocketPool(wifi.radio)
    return adafruit_requests.Session(pool, ssl.create_default_context())

def setup_button(pin):
    button = DigitalInOut(pin)
    button.direction = Direction.INPUT
    button.pull = Pull.UP
    return button

def debounce(button):
    if not button.value:
        time.sleep(0.1)
        return True
    return False

def do_button_a():
    global display
    global rgb_led
    print("Button A Pressed. Fetching Weather")
    display.paint_screen(0xff0000)
    rgb_led.set(0xff, 0, 0)
    response = weather.fetch(requests)
    # For Debugging
    weather.print(response)
    time.sleep(2)

def do_button_b():
    global display
    global rgb_led
    print("Button B Pressed")
    display.paint_screen(0x00ff00)
    rgb_led.set(0, 0xff, 0)
    time.sleep(2)

def do_button_x():
    global display
    global rgb_led
    print("Button X Pressed")
    display.paint_screen(0xff00ff)
    rgb_led.set(0xff, 0, 0xff)
    time.sleep(2)

def do_button_y():
    global display
    global rgb_led
    print("Button Y Pressed")
    display.paint_screen(0x00ffff)
    rgb_led.set(0, 0xff, 0xff)
    time.sleep(2)

print("==============================")
print("Initializing")
print("uname: ", end=" ")
print(os.uname())

# Release any resources currently in use for the displays
# Prevents error "ValueError: GP18 in use" when initializing SPI
displayio.release_displays()

spi_mosi = board.GP19
spi_clk = board.GP18

"""
classbusio.SPI(clock: microcontroller.Pin,
                MOSI: Optional[microcontroller.Pin] = None,
                MISO: Optional[microcontroller.Pin] = None)
"""
spi = busio.SPI(spi_clk, MOSI=spi_mosi)
print("SPI initialized")
display = picodisplay.screen(spi)
weather = openweather()
# rgb_led = rgb.RGB()
# Disable the LED, it seems to interfere with the WiFi?
rgb_led = rgb.FakeRGB()
rgb_led.off()

requests = init_wifi(spi)

button_a = setup_button(board.GP12)
button_b = setup_button(board.GP13)
button_x = setup_button(board.GP14)
button_y = setup_button(board.GP15)

display.paint_screen()

print("Initialization complete.")
print("------------------------------")

# Main loop
while True:
    rgb_led.off()
    time.sleep(.1)
    # Check the buttons
    if (debounce(button_a)):
        do_button_a()
    elif (debounce(button_b)):
        do_button_b()
    elif (debounce(button_x)):
        do_button_x()
    elif (debounce(button_y)):
        do_button_y()


