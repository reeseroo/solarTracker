#current power in summary


try:
        import RPi.GPIO as GPIO
except ImportError:
        import Mock.GPIO as GPIO

import time

bluePin = 14

GPIO.setmode(GPIO.BCM)
GPIO.setup(bluePin, GPIO.OUT)

GPIO.output(bluePin, GPIO.HIGH)

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