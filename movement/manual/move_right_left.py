# all of the methods here are deprecated
# the movement function has been transfered to the ESP32-C3

import RPi.GPIO as GPIO
import time
import sys
import warnings

def deprecated(func):
    def wrapper(*args, **kwargs):
        warnings.warn(f"{func.__name__} is deprecated.", DeprecationWarning)
        return func(*args, **kwargs)
    return wrapper

if len(sys.argv) != 0:
    arg_speed = int(sys.argv[1])
    direction = int(sys.argv[2])
else:
    arg_speed = 20

GPIO.setmode(GPIO.BCM)

left_servo_pins = [18, 19]
right_servo_pins = [20, 21]

left_pwm_objects = []
right_pwm_objects = []

for pin in left_servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50) 
    pwm.start(0)
    left_pwm_objects.append(pwm)
    
for pin in right_servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50) 
    pwm.start(0)
    right_pwm_objects.append(pwm)

@deprecated
# Function to set speed for a group of servos
def set_speed(servos, speed):
    
    for pwm in servos:
        if speed < 0:
            duty_cycle = (abs(speed) / 100) * 10 + 5 
        else:
            duty_cycle = (speed / 100) * 10 + 5 

        duty_cycle = max(0, min(duty_cycle, 10))
        pwm.ChangeDutyCycle(duty_cycle)

try:
    if direction == 0:
        set_speed(left_pwm_objects, 20)
        set_speed(right_pwm_objects, 25)
    else:
		set_speed(left_pwm_objects, 25)
		set_speed(right_pwm_objects, 20)
    time.sleep(1)

    set_speed(left_pwm_objects, 0)
    set_speed(right_pwm_objects, 0)

except KeyboardInterrupt:
    pass

for pwm in left_pwm_objects:
    pwm.stop()
for pwm in right_pwm_objects:
	pwm.stop()

GPIO.cleanup()
