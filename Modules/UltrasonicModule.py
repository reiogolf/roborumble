import RPi.GPIO as GPIO
import time

# Declare GPIO pins
TRIG_PIN = 37
ECHO_PIN = 35


def setupUltrasonicSensorIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(TRIG_PIN, GPIO.OUT)
    GPIO.setup(ECHO_PIN, GPIO.IN)


def detectObject():
    pulse_start = 0
    pulse_end = 0
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)
    count = 0
    # Measure the duration of the echo
    while GPIO.input(ECHO_PIN) == 0:
        count += 1
        pulse_start = time.time()
        if count > 2000:
            break
    count = 0
    while GPIO.input(ECHO_PIN) == 1:
        count += 1
        pulse_end = time.time()
        if count > 2000:
            break

    # Calculate distance to object in centimeters
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    return distance
