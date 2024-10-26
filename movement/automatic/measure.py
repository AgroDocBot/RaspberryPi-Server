import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

TRIG_LEFT = 23
ECHO_LEFT = 24
TRIG_RIGHT = 27
ECHO_RIGHT = 22

def measure_distance(trig, echo):
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.output(trig, True)
    time.sleep(0.00001)
    GPIO.output(trig, False)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    time_elapsed = stop_time - start_time
    distance = (time_elapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        left_distance = measure_distance(TRIG_LEFT, ECHO_LEFT)
        right_distance = measure_distance(TRIG_RIGHT, ECHO_RIGHT)
        print(f"{left_distance},{right_distance}")
    except KeyboardInterrupt:
        GPIO.cleanup()
    finally:
        GPIO.cleanup()
