from UltrasonicModule import *

print("Testing Ultrasonic Module")
# This test script prints the sensor readings to the console if they change

setupUltrasonicSensorIO()
try:
    while True:
        print(detectObject())
        time.sleep(0.1)  # Sleep for a while
except KeyboardInterrupt:
    GPIO.cleanup()
