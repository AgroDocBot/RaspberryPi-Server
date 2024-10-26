# all of the methods here are deprecated
# the movement function has been transfered to the ESP32-C3
# (see the ESP32-C3 Firmware repository)

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
else:
    arg_speed = 20

GPIO.setmode(GPIO.BCM)

servo_pins = [18, 19, 20, 21]

pwm_objects = []
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50) 
    pwm.start(0)
    pwm_objects.append(pwm)

@deprecated
def set_speed_all(servos, speed):
    
    for pwm in servos:
        if speed < 0:
            duty_cycle = (abs(speed) / 100) * 10 + 5 
        else:
            duty_cycle = (speed / 100) * 10 + 5 

        duty_cycle = max(0, min(duty_cycle, 10))
        pwm.ChangeDutyCycle(duty_cycle)

try:
 
    set_speed_all(pwm_objects, arg_speed)
    time.sleep(1)

    set_speed_all(pwm_objects, 0)

except KeyboardInterrupt:
    pass

for pwm in pwm_objects:
    pwm.stop()

GPIO.cleanup()
