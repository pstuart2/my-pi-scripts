import RPi.GPIO as GPIO
import time
import configparser
import requests

EffectsServer = ""
MotionPin = 4  # Input for HC-SR501
LastMovementState = 0


def setup():
    global EffectsServer, MotionPin

    print("> Set up")
    config = configparser.ConfigParser()
    config.read('config.ini')

    EffectsServer = config['DEFAULT']['EffectsServer']
    MotionPin = int(config['motion']['MotionPin'])

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(MotionPin, GPIO.IN)  # Read output from PIR motion sensor


def state_change(channel):
    global LastMovementState

    if LastMovementState == 0:
        LastMovementState = 1
    else:
        LastMovementState = 0

    send(LastMovementState)


def loop():
    GPIO.add_event_detect(MotionPin, GPIO.BOTH, callback=state_change)

    while True:
        time.sleep(10)


def send(has_motion):
    global EffectsServer

    print('Sending motion: ' + str(has_motion))

    r = requests.post(EffectsServer + "/motion", json={"hasMotion": has_motion})
    if r.status_code != 200:
        print("send_command Status: " + str(r.status_code))


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
