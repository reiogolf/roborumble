#from Modules.CameraModule import *
from Modules.MotorModule import *
from Modules.SensorModule import *
from Modules.UltrasonicModule import *
import RPi.GPIO as GPIO

INIT_TURN_TIME = 0.06  # Used to turn 45 degrees -ish
STEPS_FOR_HOME = 6

nodesFound = []
actionsMade = ""


def setupIO():
    GPIO.setmode(GPIO.BOARD)
    setupMotorIO()
    setupSensorIO()
    setupUltrasonicSensorIO()


def stopRotation():
    sensorVal = getSensorReadings()
    if (sensorVal[S2] == 1 or sensorVal[S3] == 1):
        return True
    else:
        return False


def turn_45_left():
    moveRightMotorForward()
    moveLeftMotorBackward()
    time.sleep(INIT_TURN_TIME)
    stay_put()


def turn_45_right():
    moveRightMotorBackward()
    moveLeftMotorForward()
    time.sleep(INIT_TURN_TIME)
    stay_put()


def turn_left():
    speedDownLeftMotor()
    speedDownRightMotor()
    # Initial turning
    while True:
        sensorVal = getSensorReadings()
        if (sensorVal[S1] == 1):
            break
        moveRightMotorForward()
        moveLeftMotorBackward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    while True:
        if (stopRotation()):
            break
        moveRightMotorForward()
        moveLeftMotorBackward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    speedUpLeftMotor()
    speedUpRightMotor()
    # print("Turn Left")


def turn_right():
    speedDownLeftMotor()
    speedDownRightMotor()
    # Initial turning
    while True:
        sensorVal = getSensorReadings()
        if (sensorVal[S4] == 1):
            break
        moveRightMotorBackward()
        moveLeftMotorForward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    while True:
        if (stopRotation()):
            break
        moveRightMotorBackward()
        moveLeftMotorForward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    speedUpLeftMotor()
    speedUpRightMotor()
    # print("Turn Right")


def adjust_left(steps=1):
    speedDownRightMotor()
    speedDownLeftMotor()
    for step in range(steps):
        moveRightMotorForward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    speedUpRightMotor()
    speedUpLeftMotor()
    # print("Adjust left")


def adjust_right(steps=1):
    speedDownLeftMotor()
    speedDownRightMotor()
    for step in range(steps):
        moveLeftMotorForward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    speedUpLeftMotor()
    speedUpRightMotor()
    # print("Adjust right")


def straight(steps=1):
    for step in range(steps):
        moveLeftMotorForward()
        moveRightMotorForward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    # print("Straight")


def back(steps=1):
    for step in range(steps):
        moveLeftMotorBackward()
        moveRightMotorBackward()
        time.sleep(SLEEP_TIME_DELAY)
        stay_put()
    # print("Back")


def turn_around():
    # print("Turn around")
    turn_right()


def unmapped():
    stay_put()
    # print("Unmapped, this should not happen")


def adjustOrMoveStraight(sensorVal):
    if (sensorVal[S2] == 0 and sensorVal[S3] == 1):
        adjust_right()
    elif (sensorVal[S2] == 1 and sensorVal[S3] == 0):
        adjust_left()
    elif (sensorVal[S2] == 1 and sensorVal[S3] == 1):
        straight()


def decideAction():
    sensorVal = getSensorReadings()
    # map sensorVal to BOT_MOVEMENT
    if (sensorVal[S2] == 0 and sensorVal[S3] == 1) or (sensorVal[S1] == 0 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 1):
        return "adjust_right"
    elif (sensorVal[S2] == 1 and sensorVal[S3] == 0) or (sensorVal[S1] == 1 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 0):
        return "adjust_left"
    elif sensorVal[S1] == 0 and sensorVal[S2] == 0 and sensorVal[S3] == 0 and sensorVal[S4] == 0:
        # Turn left and check
        turn_45_left()
        time.sleep(SLEEP_TIME_DELAY)
        sensorValLeft = getSensorReadings()
        # Undo left turn then turn right and check
        turn_45_right()
        turn_45_right()
        time.sleep(SLEEP_TIME_DELAY)
        sensorValRight = getSensorReadings()
        # Undo right turn
        turn_45_left()
        if (sensorValLeft[S1] == 0 and sensorValLeft[S2] == 0 and sensorValLeft[S3] == 0 and sensorValLeft[S4] == 0) and (sensorValRight[S1] == 0 and sensorValRight[S2] == 0 and sensorValRight[S3] == 0 and sensorValRight[S4] == 0):
            return "dead_end"
        else:
            return ""

    nextReading = ""
    sensorValNew = None
    leftTurnedOn = sensorVal[S1] == 1
    rightTurnedOn = sensorVal[S4] == 1
    if sensorVal[S1] == 1 or sensorVal[S4] == 1:
        stepsMoved = 0
        while True:
            sensorValNew = getSensorReadings()
            adjustOrMoveStraight(sensorValNew)
            stepsMoved += 1
            leftTurnedOn = leftTurnedOn or sensorValNew[S1] == 1
            rightTurnedOn = rightTurnedOn or sensorValNew[S4] == 1
            # Move until the track gets passed over
            if (sensorVal[S1] == 1 and sensorValNew[S1] == 0) or (sensorVal[S4] == 1 and sensorValNew[S4] == 0) or stepsMoved == STEPS_FOR_HOME:
                # move just one more step
                adjustOrMoveStraight(sensorValNew)
                sensorValNew = getSensorReadings()
                break
        if leftTurnedOn:
            nextReading = nextReading + "left"
        if rightTurnedOn:
            nextReading = nextReading + "right"
        # print("Exited at", stepsMoved)
        if (stepsMoved == STEPS_FOR_HOME and nextReading == "leftright" and sensorValNew[S2] == 1 and sensorValNew[S3] == 1):
            return "stay"
        if sensorValNew[S2] == 1 or sensorValNew[S3] == 1:
            nextReading = nextReading + "straight"
        return nextReading

    elif sensorVal[S2] == 1 and sensorVal[S3] == 1:
        return "straight"

    return ""


def act():
    decision = decideAction()
    if decision != "straight" and decision != "adjust_left" and decision != "adjust_right":
        print(decision)

    if decision == "straight":
        straight()
    elif decision == "adjust_left":
        adjust_left()
    elif decision == "adjust_right":
        adjust_right()
    elif decision == "left":
        turn_left()
    elif decision == "right":
        turn_right()
    elif decision == "dead_end":
        turn_around()
    elif decision == "stay":
        stay_put()
        return True
        return True  # Stop
    elif decision == "leftright":
        turn_right()
    elif decision == "leftstraight":
        straight()
    elif decision == "rightstraight":
        turn_right()
    elif decision == "leftrightstraight":
        turn_right()
    else:
        unmapped()


print("Starting program")
setupIO()
try:
    stay_put()
    while True:
        # Bot running
        #if (detectObject() < 30):
        #    print("Detected obj")
        if (act()):
            break

    decision = decideAction()

    while(decision != "straight"):
        decision = decideAction()
        
    while True:
        if (act()):
            break

except KeyboardInterrupt:
    GPIO.cleanup()
