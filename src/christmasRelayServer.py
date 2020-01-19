import RPi.GPIO as GPIO
import os
import time
import datetime
import logging

pins = [2, 3, 4, 17, 27, 22, 10, 9]


class ScriptItem:
    time_until = 0
    off = []
    on = []

    def __init__(self, time_until, off, on):
        self.time_until = time_until
        self.off = off
        self.on = on


basic_sequence_time = 2
drum_time = 0.2
rock_you_pause_1 = 0.2
rock_you_pause_2 = 0.8

turn_on = ScriptItem(0.0, [], [0, 1, 2])
turn_off = ScriptItem(0.0, [0, 1, 2], [])

single_on_sequence = [
    ScriptItem(basic_sequence_time, [2], [0]),
    ScriptItem(basic_sequence_time, [0], [1]),
    ScriptItem(basic_sequence_time, [1], [2]),
]

single_off_sequence = [
    ScriptItem(basic_sequence_time, [0], [1, 2]),
    ScriptItem(basic_sequence_time, [1], [0, 2]),
    ScriptItem(basic_sequence_time, [2], [0, 1]),
]

rock_you = [
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [2]),
    ScriptItem(rock_you_pause_2, [2], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [2]),
    ScriptItem(rock_you_pause_2, [2], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [0, 1]),
    ScriptItem(rock_you_pause_1, [0, 1], []),
    ScriptItem(drum_time, [], [2]),
    ScriptItem(rock_you_pause_2, [2], []),
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

sequences = [
    single_on_sequence,
    single_off_sequence,
    on_off_fifo,
    on_off_lifo,
    on_off_lifo_rev,
    rock_you,
]


def setup():
    ts = datetime.datetime.now()

    epoc = time.time()
    file_dir = os.path.dirname(os.path.realpath(__file__))
    logging.basicConfig(filename=file_dir + '/christmasRelayServer.' + str(epoc) + '.log', level=logging.INFO,
                        format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')

    logging.info('Run Start: {}'.format(ts))

    GPIO.setmode(GPIO.BCM)

    for pin in pins:
        GPIO.setup(pin, GPIO.OUT)
        pin_off(pin)


def pin_off(pin):
    GPIO.output(pin, True)


def pin_on(pin):
    GPIO.output(pin, False)


def loop():
    while True:
        for sequence in sequences:
            if is_time_to_stop():
                break

            run_sequence(20, sequence)

            minutes = 5
            while minutes > 0:
                if is_time_to_stop():
                    break

                run_item(turn_on)
                minutes = minutes - 1

            if is_time_to_stop():
                break


def is_time_to_stop():
    timestamp = get_time()

    if timestamp.hour >= 22 and timestamp.minute >= 0:
        return True

    return False


def run_sequence(times, sequence):
    run_item(turn_off)

    count = times

    while count > 0:
        logging.info('run_sequence(): count: {}'.format(count))
        count = count - 1

        for t in sequence:
            run_item(t)


def get_time():
    timestamp = datetime.datetime.now().time()
    logging.info('Time: {}'.format(timestamp))

    return timestamp


def run_item(t):
    logging.debug('Sequence...{} {} {}'.format(t.time_until, t.off, t.on))

    for i in t.off:
        pin_off(pins[i])

    for i in t.on:
        pin_on(pins[i])

    time.sleep(t.time_until)


def destroy():
    logging.info("> Clean up")
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':  # Program start from here
    setup()

    try:
        loop()
    except KeyboardInterrupt:
        pass
    finally:
        destroy()
