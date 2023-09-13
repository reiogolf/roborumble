import time
import RPi.GPIO as GPIO

# Right motor
MOTOR_RIGHT_ENABLE = 33 
MOTOR_RIGHT_PINA = 31
MOTOR_RIGHT_PINB = 29

# Left motor
MOTOR_LEFT_ENABLE = 32
MOTOR_LEFT_PINA = 36
MOTOR_LEFT_PINB = 38

TURN_TIME = 0.25

PWM_SETUP_VALUE = 1000 
TURN_SPEED_DIFF = 10
MAX_MOTOR_SPEED  = 100 - TURN_SPEED_DIFF
MIN_MOTOR_SPEED = 40

LEFT_MOTOR_SPEED = None
RIGHT_MOTOR_SPEED = None

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO.setup(MOTOR_RIGHT_ENABLE, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_PINA, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_PINB, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_ENABLE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_PINA, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_PINB, GPIO.OUT)

GPIO.output(MOTOR_RIGHT_PINA, 0)
GPIO.output(MOTOR_RIGHT_PINB, 0)

LEFT_MOTOR_SPEED = GPIO.PWM(MOTOR_LEFT_ENABLE, PWM_SETUP_VALUE)
RIGHT_MOTOR_SPEED = GPIO.PWM(MOTOR_RIGHT_ENABLE, PWM_SETUP_VALUE)

LEFT_MOTOR_SPEED.start(MIN_MOTOR_SPEED)
RIGHT_MOTOR_SPEED.start(MIN_MOTOR_SPEED)

MOTOR_SPEED = MIN_MOTOR_SPEED

MAX_RADIUS = 7
MAX_X = 7
MAX_Y = 7

def setMotorSpeed(val):
    if val >= MIN_MOTOR_SPEED and val <= MAX_MOTOR_SPEED:
        MOTOR_SPEED = val
        print("MOTOR_SPEED",MOTOR_SPEED)
        LEFT_MOTOR_SPEED.start(MOTOR_SPEED)
        RIGHT_MOTOR_SPEED.start(MOTOR_SPEED)

def stay_put():
    GPIO.output(MOTOR_LEFT_PINA, 0)
    GPIO.output(MOTOR_LEFT_PINB, 0)
    GPIO.output(MOTOR_RIGHT_PINA, 0)
    GPIO.output(MOTOR_RIGHT_PINB, 0)
    print("Stay put")


def rightMotorForword():    
    GPIO.output(MOTOR_RIGHT_PINA, 1)
    GPIO.output(MOTOR_RIGHT_PINB, 0)

def leftMotorForword():    
    GPIO.output(MOTOR_LEFT_PINA, 1)
    GPIO.output(MOTOR_LEFT_PINB, 0)

def rightMotorBackword():    
    GPIO.output(MOTOR_RIGHT_PINA, 0)
    GPIO.output(MOTOR_RIGHT_PINB, 1)

def leftMotorBackword():    
    GPIO.output(MOTOR_LEFT_PINA, 0)
    GPIO.output(MOTOR_LEFT_PINB, 1)


def front():
    rightMotorForword()
    leftMotorForword()
    print("Move Front")


def back():
    rightMotorBackword()
    leftMotorBackword()
    print("Move Back")


def left():
    rightMotorForword()
    leftMotorBackword()
    print("Move Left")


def right():
    leftMotorForword()
    rightMotorBackword()
    print("Turn right")

def moveFrontRight():
    LEFT_MOTOR_SPEED.start(MOTOR_SPEED+TURN_SPEED_DIFF)
    RIGHT_MOTOR_SPEED.start(MOTOR_SPEED)
    print("Turn front right")
    front()

def moveFrontLeft():
    LEFT_MOTOR_SPEED.start(MOTOR_SPEED)
    RIGHT_MOTOR_SPEED.start(MOTOR_SPEED+TURN_SPEED_DIFF)
    print("Turn front left")
    front()

def moveBackRight():
    LEFT_MOTOR_SPEED.start(MOTOR_SPEED+TURN_SPEED_DIFF)
    RIGHT_MOTOR_SPEED.start(MOTOR_SPEED)
    print("Turn Back right")
    back()

def moveBackLeft():
    LEFT_MOTOR_SPEED.start(MOTOR_SPEED)
    RIGHT_MOTOR_SPEED.start(MOTOR_SPEED+TURN_SPEED_DIFF)
    print("Turn Back left")
    back()

def mapSpeedValue(val):
    original_min = 0
    original_max = MAX_RADIUS
    target_min = MIN_MOTOR_SPEED
    target_max = MAX_MOTOR_SPEED

    # Perform the linear mapping
    mapped_value = ((val - original_min) / (original_max - original_min)) * (target_max - target_min) + target_min

    # Print the mapped value
    if mapped_value > MAX_MOTOR_SPEED:
        mapped_value = MAX_MOTOR_SPEED
    if mapped_value < MIN_MOTOR_SPEED:
        mapped_value = MIN_MOTOR_SPEED    
    return int(mapped_value)



def analogMove(x,y,radius):
    
    # Calculate motor speeds
    rightMotorSpeed = radius - x
    leftMotorSpeed = radius + x
    print(mapSpeedValue(rightMotorSpeed), mapSpeedValue(leftMotorSpeed))

    # Set motor speeds and directions (implementation depends on your hardware)
    LEFT_MOTOR_SPEED.start(mapSpeedValue(leftMotorSpeed))
    RIGHT_MOTOR_SPEED.start(mapSpeedValue(rightMotorSpeed))
    print("")

    # Set motor directions 
    if y > 0:
       front()
    elif y < 0:
       back()

   
