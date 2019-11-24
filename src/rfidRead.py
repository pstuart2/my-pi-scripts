# https://pimylifeup.com/raspberry-pi-rfid-rc522/

import RPi.GPIO as GPIO
import SimpleMFRC522
import configparser
import requests
import time

EffectsServer = ""
DelayAfterRead = 5

reader = SimpleMFRC522.SimpleMFRC522()


def setup():
    global EffectsServer, DelayAfterRead

    print("> Set up")
    config = configparser.ConfigParser()
    config.read('config.ini')

    EffectsServer = config['DEFAULT']['EffectsServer']
    DelayAfterRead = int(config['rfid']['DelayAfterRead'])


def loop():
    global DelayAfterRead
    while True:
        print('Reading...')
        id, text = reader.read()
        send(id, text)
        time.sleep(DelayAfterRead)


def send(rfid_id, rfid_text):
    global EffectsServer

    print('Sending : ' + str(rfid_id) + ' / ' + rfid_text)

    r = requests.post(EffectsServer + "/rfid", json={"id": rfid_id, "text": rfid_text})
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
