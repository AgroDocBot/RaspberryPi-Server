import RPi.GPIO as GPIO
import time
import sys

position_file = "last_pos.txt"
stop_signal_file = "stop_signal.txt"

servo_pin = 17
step = 5

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def read_angle_from_file():
    try:
        with open(position_file, "r") as file:
            return int(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def write_angle_to_file(angle):
    with open(position_file, "w") as file:
        file.write(str(angle))

def set_angle(angle):
    duty_cycle = 2 + (angle / 18)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.15)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)
    write_angle_to_file(angle)

def set_stop_signal(value):
    with open(stop_signal_file, "w") as file:
        file.write(str(value))

def should_stop():
    try:
        with open(stop_signal_file, "r") as file:
            return file.read().strip() == "1"
    except FileNotFoundError:
        return False

arg_req = int(sys.argv[1])
current_angle = read_angle_from_file()

try:
    if arg_req == 0:  
        set_stop_signal(1)  
    elif arg_req in [1, -1]: 
        set_stop_signal(0)  
        while 0 <= current_angle <= 180:
            if should_stop():
                break
            print(f"Moving to {current_angle}°")
            set_angle(current_angle)
            current_angle += step if arg_req == 1 else -step
    elif arg_req == 2:  
        set_stop_signal(0)  
        set_angle(180)
    elif arg_req == -2:  
        set_stop_signal(0)  
        set_angle(0)
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    pwm.stop()
    GPIO.cleanup()
