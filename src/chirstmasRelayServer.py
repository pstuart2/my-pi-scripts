import RPi.GPIO as GPIO
import time
from bottle import Bottle, run, post, request

pins = [2, 3, 4, 17, 27, 22, 10, 9]

app = Bottle()


class ScriptItem:
    time_until = 0
    off = []
    on = []

    def __init__(self, time_until, off, on):
        self.time_until = time_until
        self.off = off
        self.on = on


basic_sequence_time = 0.5
drum_time = 0.2
rock_you_pause_1 = 0.2
rock_you_pause_2 = 0.8

turn_on = ScriptItem(0.0, [], [0, 1, 2])
turn_off = ScriptItem(0.0, [0, 1, 2], [])

one_second_sequence = [
    ScriptItem(basic_sequence_time, [2], [0]),
    ScriptItem(basic_sequence_time, [0], [1]),
    ScriptItem(basic_sequence_time, [1], [2]),
]

rock_you = [
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [2]),
    ScriptItem(rock_you_pause_2, [2], []),
]

on_off_fifo = [
    ScriptItem(basic_sequence_time, [], [0]),
    ScriptItem(basic_sequence_time, [], [1]),
    ScriptItem(basic_sequence_time, [], [2]),
    ScriptItem(basic_sequence_time, [0], []),
    ScriptItem(basic_sequence_time, [1], []),
    ScriptItem(basic_sequence_time, [2], []),
]

on_off_lifo = [
    ScriptItem(basic_sequence_time, [], [0]),
    ScriptItem(basic_sequence_time, [], [1]),
    ScriptItem(basic_sequence_time, [], [2]),
    ScriptItem(basic_sequence_time, [2], []),
    ScriptItem(basic_sequence_time, [1], []),
    ScriptItem(basic_sequence_time, [0], []),
]

on_off_lifo_rev = [
    ScriptItem(basic_sequence_time, [], [2]),
    ScriptItem(basic_sequence_time, [], [1]),
    ScriptItem(basic_sequence_time, [], [0]),
    ScriptItem(basic_sequence_time, [0], []),
    ScriptItem(basic_sequence_time, [1], []),
    ScriptItem(basic_sequence_time, [2], []),
]


def setup():
    GPIO.setmode(GPIO.BCM)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, True)


@post('/lights')
def lights():
    data = request.json

    for i in range(len(data)):
        if data[i] == 0:
            GPIO.output(pins[i], True)
        else:
            GPIO.output(pins[i], False)

    return ""


def loop():
    run_sequence(5, on_off_lifo_rev)


# run(app, host='localhost', port=8080)
def run_sequence(times, sequence):
    run_item(turn_off)

    count = times

    while count > 0:
        print('run_sequence(): count: {}'.format(count))
        count = count - 1

        for t in sequence:
            run_item(t)


def run_item(t):
    print('Sequence...{} {} {}'.format(t.time_until, t.off, t.on))

    for i in t.off:
        GPIO.output(pins[i], True)

    for i in t.on:
        GPIO.output(pins[i], False)

    time.sleep(t.time_until)


def destroy():
    print("> Clean up")
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        pass
    finally:
        destroy()
