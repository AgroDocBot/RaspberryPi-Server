import RPi.GPIO as GPIO
import time

arg_speed = int(sys.argv[1])

servo_pin = 15  
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)  
pwm.start(0)  

try:
    
    pwm.ChangeDutyCycle(arg_speed)
    time.sleep(1)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()