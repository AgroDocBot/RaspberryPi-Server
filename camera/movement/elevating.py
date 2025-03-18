import RPi.GPIO as GPIO
import time
import sys

arg_speed = float(sys.argv[1])
arg_time = float(sys.argv[2])

servo_pin = 18  
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  
pwm.start(0)  

try:
    
    pwm.ChangeDutyCycle(arg_speed)
    time.sleep(arg_time)
    pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)


except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
