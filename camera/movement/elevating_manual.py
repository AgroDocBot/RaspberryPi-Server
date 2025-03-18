import RPi.GPIO as GPIO
import time
import sys

servo_pin = 18
position_file = "camera_level.txt"

GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

pwm = GPIO.PWM(servo_pin, 50)
pwm.start(7.5)

arg_speed = float(sys.argv[1])  # Servo speed
arg_time = float(sys.argv[2])   # Duration to run the servo

# Read/Write Position Functions
def read_level():
    try:
        with open(position_file, "r") as file:
            return float(file.read().strip())
    except (FileNotFoundError, ValueError):
        return 0.0

def write_level(level):
    with open(position_file, "w") as file:
        file.write(f"{level:.2f}")

current_level = read_level()
step_duration = 0.1
step_change = (step_duration / arg_time) * (1 if arg_speed < 7.5 else -1)

try:
    pwm.ChangeDutyCycle(arg_speed)
    for _ in range(int(arg_time / step_duration)):
        new_level = current_level + step_change
        
        if 0.0 <= new_level <= 1.0:
            current_level = new_level
            write_level(current_level)
            time.sleep(step_duration)
        else:
            print("Reached limit")
            break
    
    pwm.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)
except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
