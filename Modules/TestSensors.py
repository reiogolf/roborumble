from SensorModule import *
import time

print("Testing Sensor Module")
# This test script prints the sensor readings to the console if they change

setupSensorIO()
storedVal = {}
try:
    while True:
        currentVal = getSensorReadings()
        if (storedVal != currentVal):
            printSensorReadings(currentVal)
            storedVal = currentVal
        time.sleep(0.01)  # Sleep for 10 milliseconds

except KeyboardInterrupt:
    GPIO.cleanup()
