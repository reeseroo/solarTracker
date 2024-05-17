#current power in summary


import RPi.GPIO as GPIO
import time

bluePin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(bluePin, GPIO.OUT)

GPIO.output(bluePin, GPIO.HIGH)

try:
        while 1:
                GPIO.output(bluePin, GPIO.LOW)
                time.sleep(0.75)
                GPIO.output(bluePin, GPIO.HIGH)
                time.sleep(0.75)
except KeyboardInterrupt:
        GPIO.cleanup()