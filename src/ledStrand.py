#!/usr/bin/env python3
import math
import time
from rpi_ws281x import *

TOP_BAR_PIXEL_COUNT = 30
VERTICAL_BAR_PIXEL_COUNT = 57
BOTTOM_BAR_PIXEL_COUNT = 30

top_bar = []
vertical_bar = []
bottom_bar = []

_rows = []

max_intensity: int = 128
build_up: int = 4
step: int = math.floor(max_intensity / build_up)

# LED strip configuration:
LED_COUNT = TOP_BAR_PIXEL_COUNT + VERTICAL_BAR_PIXEL_COUNT + BOTTOM_BAR_PIXEL_COUNT
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53


def setup(rows):
    global top_bar, vertical_bar, bottom_bar

    for i in range(0, TOP_BAR_PIXEL_COUNT):
        top_bar.append(i)

    next_start = TOP_BAR_PIXEL_COUNT
    for i in range(next_start, next_start + VERTICAL_BAR_PIXEL_COUNT):
        vertical_bar.append(i)

    next_start = next_start + VERTICAL_BAR_PIXEL_COUNT

    for i in range(next_start, next_start + BOTTOM_BAR_PIXEL_COUNT):
        bottom_bar.append(i)

    rows.append(top_bar)

    for i in vertical_bar:
        rows.append([i])

    rows.append(bottom_bar)


def floor_down(strip, rows, throttle=0):
    global max_intensity, build_up, step

    row_count: int = len(rows)
    end: int = 0 - build_up - 1
    start: int = row_count + build_up - 1

    for current_full_row in range(start, end, -1):
        render_frame(strip, rows, row_count, current_full_row, throttle)


def floor_up(strip, rows, throttle=0):
    global max_intensity, build_up, step

    row_count: int = len(rows)
    start: int = 0 - build_up
    end: int = row_count + build_up

    for current_full_row in range(start, end):
        render_frame(strip, rows, row_count, current_full_row, throttle)


def render_frame(strip, rows, row_count, current_full_row, throttle):
    global max_intensity, build_up, step

    for diff in range(-build_up, build_up + 1):
        current_row: int = current_full_row + diff
        if 0 <= current_row < row_count:
            intensity: int = min((max_intensity - abs(step * diff)), 255)

            for pixel in rows[current_row]:
                strip.setPixelColor(pixel, Color(intensity, intensity, intensity))

    strip.show()
    time.sleep(throttle / 1000)


def move_floor(strip, rows, floors, dir_func):
    speeds = [40, 20, 10, 5]

    if floors == 1:
        dir_func(strip, rows, speeds[0])
        return

    full_speed_floors: int = floors - (len(speeds) * 2)

    if full_speed_floors >= 0:
        for i in range(0, len(speeds)):
            dir_func(strip, rows, speeds[i])

        for i in range(0, full_speed_floors):
            dir_func(strip, rows, 0)

        for i in range(len(speeds) - 1, -1, -1):
            dir_func(strip, rows, speeds[i])
    else:
        half_floors: int = math.floor(floors / 2)
        odd_floors: bool = floors % 2 > 0
        speed: int = 0

        for i in range(0, half_floors):
            speed = i
            dir_func(strip, rows, speeds[i])

        if odd_floors:
            dir_func(strip, rows, speeds[speed])

        for i in range(speed, -1, -1):
            dir_func(strip, rows, speeds[i])


# Define functions which animate LEDs in various ways.
def set_bar_color(strip, color, pixels):
    """Wipe color across display a pixel at a time."""
    for i in pixels:
        strip.setPixelColor(i, color)

    strip.show()


def destroy(strip):
    print("> Clean up")
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, Color(0, 0, 0))
        strip.show()


# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    _strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, WS2812_STRIP)
    # Initialize the library (must be called once before other functions).
    _strip.begin()

    print('Press Ctrl-C to quit.')

    try:
        setup(_rows)

        move_floor(_strip, _rows, 3, floor_up)
        time.sleep(2)
        move_floor(_strip, _rows, 8, floor_up)
        time.sleep(2)
        move_floor(_strip, _rows, 11, floor_down)


    except KeyboardInterrupt:
        pass

    finally:
        destroy(_strip)
