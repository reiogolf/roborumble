import math
from enum import Enum

ActionBtnByte = 5
ArrowBtnByte = 6

class GamePadMode(Enum):
    DIGITAL= 0
    JOYSTICK= 1

class GamePadActionBtn(Enum):
    # Byte 6
    START_BIT= 0
    SELECT_BIT= 1
    TRIANGLE_BIT= 2 
    CIRCLE_BIT= 3
    CROSS_BIT= 4
    SQUARE_BIT= 5

class GamePadArrowBtn(Enum):
    # Byte 7 in case of Digital Mode GamePad
    UP_BIT= 0
    DOWN_BIT= 1
    LEFT_BIT= 2
    RIGHT_BIT= 3

class GamePadBtnReleased(Enum):
    RELEASED_BIT= 11


def decodeAngleRadius(value):
    angle = (value >> 3) * 15
    radius = value & 0x07
    x_value = radius * math.cos(math.radians(angle))
    y_value = radius * math.sin(math.radians(angle))
    return x_value, y_value, radius

def getGamePadMode(packet):
    if packet[0] == 255 and packet[1] == 1 and packet[2] == 1 and packet[3] == 1 and packet[4] == 2:
        return GamePadMode.DIGITAL
    elif packet[0] == 255 and packet[1] == 1 and packet[2] == 2 and packet[3] == 1 and packet[4] == 2:
        return GamePadMode.JOYSTICK
    else :
        return None

def isGamePadChanged(packet):
    if packet[0] == 255 and packet[1] == 0 and packet[2] == 2 and packet[3] == 1 and packet[4] == 2 and packet[5] == 1:
        return True
    else:
        return False
       

def isUpBtnPressed(value):
    return not not value & (1 << GamePadArrowBtn.UP_BIT.value)

def isDownBtnPressed(value):
    return not not value & (1 << GamePadArrowBtn.DOWN_BIT.value)

def isRightBtnPressed(value):
    return not not value & (1 << GamePadArrowBtn.RIGHT_BIT.value)

def isLeftBtnPressed(value):
    return not not value & (1 << GamePadArrowBtn.LEFT_BIT.value)

def isUpAndRightBtnPressed(value):
    return isUpBtnPressed(value) and isRightBtnPressed(value)

def isUpAndLeftBtnPressed(value):
    return isUpBtnPressed(value) and isLeftBtnPressed(value)

def isDownAndRightBtnPressed(value):
    return isDownBtnPressed(value) and isRightBtnPressed(value)

def isDownAndLeftBtnPressed(value):
    return isDownBtnPressed(value) and isLeftBtnPressed(value)

def isStartBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.START_BIT.value)

def isSelectBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.SELECT_BIT.value)

def isTriangleBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.TRIANGLE_BIT.value)

def isCircleBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.CIRCLE_BIT.value)

def isCrossBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.CROSS_BIT.value)

def isSquareBtnPressed(value):
    return not not value & (1 << GamePadActionBtn.SQUARE_BIT.value)

def isButtonPressed(gamePadMode,packet):
    if gamePadMode == GamePadMode.DIGITAL:
        for arrowBtn in GamePadArrowBtn:
            if packet[6] == arrowBtn.value:
                return arrowBtn
    
    if gamePadMode == GamePadMode.JOYSTICK:
        print("packet[6]:", packet[6])
        joystickValues = decodeAngleRadius(packet[6])
        print("joystick Values: ", joystickValues)
        print("")

    for actionBtn in GamePadActionBtn:
        if packet[5] == actionBtn.value:
            return actionBtn
    
    if packet[5] == 0 and packet[6] == 0 and packet[7] == 0:
        return  GamePadBtnReleased.BTN_RELEASED
    
    return None    



def decodeGamepadData(packet):
    
    PI = 3.14159
    print("packet len:", len(packet))

    if len(packet) == 8:  
        gamePadMode = getGamePadMode(packet)
        print("Game Pad Mode: ",gamePadMode)
        btnPressed = None
        if gamePadMode == GamePadMode.DIGITAL or gamePadMode == GamePadMode.JOYSTICK : 
            btnPressed = isButtonPressed(gamePadMode, packet)
            print("Action btn:", btnPressed )        
            print("")
        
        return btnPressed
    else:
        return None
