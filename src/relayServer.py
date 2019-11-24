import RPi.GPIO as GPIO
from bottle import Bottle, run, post, request

pins = [2, 3, 4, 17, 27, 22, 10, 9]

app = Bottle()


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
    run(app, host='localhost', port=8080)


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
