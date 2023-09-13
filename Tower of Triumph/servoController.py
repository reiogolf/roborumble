import RPi.GPIO as GPIO
import time
from enum import Enum


class ServoState(Enum):
    CLOSED = 95
    OPEN = 180

class Servo:
    def __init__(self, pin, frequency=50, angle_range=(ServoState.CLOSED.value, ServoState.OPEN.value), duty_cycle_range=(2.5, 12.5), servo_state = ServoState.CLOSED):
        self.pin = pin
        self.frequency = frequency
        self.angle_range = angle_range
        self.duty_cycle_range = duty_cycle_range
        self.servo_state = ServoState.CLOSED
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.pin, self.frequency)
        self.pwm.start(0)
        self.set_angle(ServoState.CLOSED.value)

    def servo_toggle(self):
        if self.servo_state == ServoState.OPEN:
            self.set_angle(ServoState.CLOSED.value)
            self.servo_state = ServoState.CLOSED
        elif self.servo_state == ServoState.CLOSED:
            self.set_angle(ServoState.OPEN.value)
            self.servo_state = ServoState.OPEN            
        
    def set_angle(self, angle):
        if angle < self.angle_range[0]:
            angle = self.angle_range[0]
        elif angle > self.angle_range[1]:
            angle = self.angle_range[1]
            
        print("Servo angle:", angle)
        duty_cycle = self.map_value(angle, *self.angle_range, *self.duty_cycle_range)
        
        self.pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2)  # Give the servo some time to reach the desired position
        
    def map_value(self, value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    
    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()

# Servo Cariblration Code
# if __name__ == "__main__":
#     try:
#         servo = Servo(pin=40)  # Replace 18 with the GPIO pin you're using
        
#         while True:
#             angle = float(input("Enter angle (0 to 180): "))
#             servo.set_position(angle)
            
#     except KeyboardInterrupt:
#         servo.cleanup()
#         print("Servo control interrupted")
