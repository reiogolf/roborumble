import RPi.GPIO as GPIO

# On track proximity sensor reading is 1
# Declare GPIO pins
SENSOR_1 = 22
SENSOR_2 = 23
SENSOR_3 = 21
SENSOR_4 = 19

# Left to Right
S1 = "One"
S2 = "Two"
S3 = "Three"
S4 = "Four"


def setupSensorIO():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(SENSOR_1, GPIO.IN)
    GPIO.setup(SENSOR_2, GPIO.IN)
    GPIO.setup(SENSOR_3, GPIO.IN)
    GPIO.setup(SENSOR_4, GPIO.IN)


def getSensorReadings():
    val = {
        S1: GPIO.input(SENSOR_1),
        S2: GPIO.input(SENSOR_2),
        S3: GPIO.input(SENSOR_3),
        S4: GPIO.input(SENSOR_4),
    }
    # printSensorReadings(val)
    return val


def printSensorReadings(sensorVal):
    print(S1 + ": " + str(sensorVal[S1]) + " " + S2 + ": " + str(sensorVal[S2]) + " " + S3 + ": " + str(sensorVal[S3]) +
          " " + S4 + ": " + str(sensorVal[S4]))
