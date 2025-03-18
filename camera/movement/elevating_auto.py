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

try:
    pwm.ChangeDutyCycle(arg_speed)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
