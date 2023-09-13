import subprocess
import serial
import time
import threading
from dabbleController import *
from motorController import *
from servoController import Servo
from FPV.vedioStreamServer import *

# Create a thread to run the StartStream() function
stream_thread = threading.Thread(target=StartStream)

SERVO_PIN = 40 # Board pin

def run_rfcomm_watch():
    try:
        # Run the bluetoothctl command to make the device discoverable
        subprocess.run(["bluetoothctl", "discoverable", "on"], check=True)

        # Run the command 'sudo rfcomm watch hci0'
        process = subprocess.Popen(['sudo', 'rfcomm', 'watch', 'hci0'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Print a message indicating the rfcomm watch is started
        print("Waiting for a device to connect...")
        
        return process
    
    except Exception as e:
        print("Error:", e)
        return None

def main():
    motorSpeed = (MAX_MOTOR_SPEED - MIN_MOTOR_SPEED)/2 + MIN_MOTOR_SPEED
    # Start the rfcomm watch process
    rfcomm_process = run_rfcomm_watch()
    streamStarted = False
    
    if rfcomm_process is not None:
        try:
            # Wait until a device is connected
            while True:
                status_output = subprocess.check_output(['sudo', 'rfcomm', '-i', 'hci0'])
                if b'rfcomm0: ' in status_output:
                    break
                time.sleep(1)
            
            print("Device connected!")

            # Open a serial connection using the rfcomm port
            ser = serial.Serial('/dev/rfcomm0', baudrate=9600, timeout=1)
            
            print("Motor Speed: ", motorSpeed)
            setMotorSpeed(motorSpeed)
            servo = Servo(pin=SERVO_PIN)  # Replace 18 with the GPIO pin you're using
            servoAngle = 80 # Angle between 80 - 180

            while True:
                # Sending data
                data_to_send = "Hello from Raspberry Pi!\r\n"
                ser.write(data_to_send.encode())
                print("Sent:", data_to_send)
                
                # Receiving data
                while ser.inWaiting:
                    # Wait for data to be received
                    received_data = ser.read(8)
                    if received_data:
                        if isGamePadChanged(received_data):
                            print("Game Pad changed !!!")
                            continue
                        gamePadMode = getGamePadMode(received_data)
                        if gamePadMode == GamePadMode.DIGITAL :
                            # Arrow Btn actions
                            value = received_data[ArrowBtnByte]
                            if isUpAndRightBtnPressed(value):
                                moveFrontRight()
                            elif isUpAndLeftBtnPressed(value):
                                moveFrontLeft()
                            elif isDownAndRightBtnPressed(value):
                                moveBackRight()
                            elif isDownAndLeftBtnPressed(value):
                                moveBackLeft()
                            elif isUpBtnPressed(value) :
                                front()                        
                            elif isDownBtnPressed(value) :
                                back()
                            elif isRightBtnPressed(value) :
                                right()
                            elif isLeftBtnPressed(value) :
                                left()

                        if gamePadMode == GamePadMode.JOYSTICK :
                            print("JOYSTICK Mode")
                            # Arrow Btn actions
                            value = received_data[ArrowBtnByte]
                            (x_value, y_value, radians) = decodeAngleRadius(value)
                            print("value")
                            print(int(x_value), int(y_value), int(radians))
                            analogMove(int(x_value), int(y_value), int(radians))

                        # Action btn actions
                        value = received_data[ActionBtnByte]
                        if isStartBtnPressed(value) and not streamStarted :
                            print("Start btn pressed")
                            stream_thread.start()
                            streamStarted = True

                        if isSelectBtnPressed(value) :
                            print("Select btn pressed")
                           

                        if isTriangleBtnPressed(value) :
                            motorSpeed = motorSpeed + 10
                            if motorSpeed > MAX_MOTOR_SPEED:
                                motorSpeed = MAX_MOTOR_SPEED
                            print("Motor Speed:", motorSpeed)
                            setMotorSpeed(motorSpeed)
                        elif isCrossBtnPressed(value) :
                            if motorSpeed < MIN_MOTOR_SPEED:
                                motorSpeed = MIN_MOTOR_SPEED  
                            motorSpeed = motorSpeed - 10
                            print("Motor Speed:", motorSpeed)
                            setMotorSpeed(motorSpeed)

                        if isCircleBtnPressed(value) :
                            servo.servo_toggle()

                        if received_data[5] == 0 and received_data[6] == 0 and received_data[7] == 0:
                            stay_put()                        

                        for byte in received_data:
                            print(byte, end =" ")
                        print("")
                
        except KeyboardInterrupt:
            # Close the serial connection
            ser.close()
            
            # Terminate the rfcomm watch process
            rfcomm_process.terminate()
            print("Exiting...")
            
        except Exception as e:
            print("Error:", e)
            if 'ser' in locals():
                ser.close()
            rfcomm_process.terminate()

if __name__ == "__main__":
    main()
