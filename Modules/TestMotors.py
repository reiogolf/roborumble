from MotorModule import *
import time

MOVE_TIME = 0.25


def front():
    moveLeftMotorForward()
    moveRightMotorForward()
    time.sleep(MOVE_TIME)
    stay_put()
    print("Move Front")


def back():
    moveLeftMotorBackward()
    moveRightMotorBackward()
    time.sleep(MOVE_TIME)
    stay_put()
    print("Move Back")


def left():
    moveRightMotorForward()
    moveLeftMotorBackward()
    time.sleep(MOVE_TIME)
    stay_put()
    print("Move Left")


def right():
    moveRightMotorBackward()
    moveLeftMotorForward()
    time.sleep(MOVE_TIME)
    stay_put()
    print("Turn right")


def testMotorSpeeds():
    # This function allows us to check motor movement with different speeds
    for i in range(10):
        print(i)
        setRightMotorSpeed(i*10)
        setLeftMotorSpeed(i*10)
        front()
        time.sleep(1)
        stay_put()


print("Testing Motor Module")
# This test script controls the motors for testing

setupMotorIO()
try:
    stay_put()
    while True:
        decision = input(
            "front(f) / back(b) / left(l) / right(r) / testSpeeds(t) - ")
        if (decision == 'f'):
            front()
        elif (decision == 'b'):
            back()
        elif (decision == 'l'):
            left()
        elif (decision == 'r'):
            right()
        elif (decision == 't'):
            testMotorSpeeds()
        else:
            GPIO.cleanup()
            exit()
        time.sleep(0.01)  # Sleep for 10 milliseconds
except KeyboardInterrupt:
    GPIO.cleanup()
