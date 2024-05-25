# yellow = 4
# green = 24
# red = 23
# white = 22
# blue = 14

try:
    import RPi.GPIO as GPIO
except ImportError:
    import Mock.GPIO as GPIO

import time
from APIHandler import new_tokens, get_access_token_and_refresh_token, latest_telemetry

bluePin = 14
yellowPin = 4
greenPin = 24
redPin = 23
whitePin = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(bluePin, GPIO.OUT)
GPIO.setup(yellowPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(whitePin, GPIO.OUT)

GPIO.output(bluePin, GPIO.LOW)
GPIO.output(yellowPin, GPIO.LOW)
GPIO.output(greenPin, GPIO.LOW)
GPIO.output(redPin, GPIO.LOW)
GPIO.output(whitePin, GPIO.LOW)

telemetryInterval = 60*10
tokenRefreshInterval = 5 * 60 * 60
tokenRefreshTime = time.time()
netProduction = latest_telemetry()
telemetryTime = time.time()

try:
    while 1:
        currentTime = time.time()
        if currentTime - tokenRefreshTime >= tokenRefreshInterval:
            new_tokens()
            tokenRefreshTime = currentTime
        if currentTime - telemetryTime >= telemetryInterval:
            netProduction = latest_telemetry()
        if netProduction <= 0:
            GPIO.output(redPin, GPIO.HIGH)
            GPIO.output(greenPin, GPIO.LOW)
            GPIO.output(yellowPin, GPIO.LOW)
            GPIO.output(whitePin, GPIO.LOW)
            GPIO.output(bluePin, GPIO.LOW)
            print("Red")
        elif netProduction > 0 and netProduction < 1000:
            GPIO.output(redPin, GPIO.LOW)
            GPIO.output(yellowPin, GPIO.HIGH)
            GPIO.output(whitePin, GPIO.LOW)
            GPIO.output(bluePin, GPIO.LOW)
            GPIO.output(greenPin, GPIO.LOW)
            print("Yellow")
        elif netProduction >= 1000 and netProduction < 2000:
            GPIO.output(redPin, GPIO.LOW)
            GPIO.output(yellowPin, GPIO.HIGH)
            GPIO.output(whitePin, GPIO.HIGH)
            GPIO.output(bluePin, GPIO.LOW)
            GPIO.output(greenPin, GPIO.LOW)
            print("White")
        elif netProduction >= 2000 and netProduction < 3000:
            GPIO.output(redPin, GPIO.LOW)
            GPIO.output(yellowPin, GPIO.HIGH)
            GPIO.output(whitePin, GPIO.HIGH)
            GPIO.output(bluePin, GPIO.HIGH)
            GPIO.output(greenPin, GPIO.LOW)
            print("Blue")
        elif netProduction >= 3000:
            GPIO.output(redPin, GPIO.LOW)
            GPIO.output(yellowPin, GPIO.HIGH)
            GPIO.output(whitePin, GPIO.HIGH)
            GPIO.output(bluePin, GPIO.HIGH)
            GPIO.output(greenPin, GPIO.HIGH)
            print("Green")
        time.sleep(telemetryInterval)
except KeyboardInterrupt and Exception as e:
    print(e)
    GPIO.cleanup()
