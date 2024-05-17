# current power in summary
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

try:
        while 1:
                GPIO.output(bluePin, GPIO.LOW)
                print("LED off")
                time.sleep(0.75)
                GPIO.output(bluePin, GPIO.HIGH)
                print("LED on")
                time.sleep(0.75)
except KeyboardInterrupt:
        GPIO.cleanup()