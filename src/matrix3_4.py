#!/usr/bin/env python3
import RPi.GPIO as GPIO
from pad4pi import rpi_gpio
import time
import requests
import configparser

EffectsServer = ""

KEYPAD = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["*", "0", "#"]
]

ROW_PINS = [5, 6, 13, 19]
COL_PINS = [26, 20, 21]


def setup():
    global EffectsServer

    print("> Setup")
    config = configparser.ConfigParser()
    config.read('config.ini')

    EffectsServer = config['DEFAULT']['EffectsServer']

    factory = rpi_gpio.KeypadFactory()
    keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
    keypad.registerKeyPressHandler(process_key)

    return keypad


def process_key(key):
    print(f'Processing key: {key}')
    r = requests.post(EffectsServer + "/keypad", json={"key": key})
    if r.status_code != 200:
        print(f'Failed to send: StatusCode: {r.status_code}')


def destroy(keypad):
    print("> Clean up")
    keypad.cleanup()


if __name__ == '__main__':
    _keypad = setup()

    print('Press Ctrl-C to quit.')

    try:
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        destroy(_keypad)
