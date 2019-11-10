"""
BinBot Tread module to provide control interface to robot kit's mechanical tread components.

Author: Sean Reddington
Date: 2019/11/8

TODO Check that left and right are mixed up

"""

import time
import RPi.GPIO as GPIO  # Linux required!


# motor_EN_A: Pin11  |  motor_EN_B: Pin7
# motor_A:  Pin13,Pin12    |  motor_B: Pin8,Pin10


Motor_A_EN = 17
Motor_B_EN = 4

Motor_A_Pin1 = 27
Motor_A_Pin2 = 18
Motor_B_Pin1 = 14
Motor_B_Pin2 = 15


Dir_forward = 0
Dir_backward = 1

left_forward = 0
left_backward = 1

right_forward = 0
right_backward = 1

pwn_A = 0
pwm_B = 0

d_scale = 0.5  # Scales sleep to unit of distance


def execute(instructions):
    for e in instructions["treads"]:
        angle = e["angle"]
        distance = e["distance"]
        speed = 60
        radius = angle / 360

        if angle == 0 or angle == 360:
            print("forward")
            _forward(distance, speed)

        elif angle == 180:
            print("backward")
            _backward(distance, speed)

        elif 0 < angle < 180:
            print("right")
            _rightTurn(distance, speed, int(speed * radius))

        elif 180 < angle < 360:
            print("left")
            radius -= 0.5
            _leftTurn(distance, speed, int(speed * radius))
        else:
            print("invalid angle")
            _motorStop()
            raise
    _motorStop()


def _forward(distance, speed):
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_forward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Moved " + str(distance) + " meters forward.\n")


def _backward(distance, speed):
    _motorLeft(1, left_backward, speed)
    _motorRight(1, right_backward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Moved " + str(distance) + " meters backward.\n")


def _rightTurn(distance, speed, radius):
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_backward, radius)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Treads turned " + str(radius*3.6) + " degrees right.\n")
    pass


def _leftTurn(distance, speed, radius):
    _motorLeft(1, left_backward, radius)
    _motorRight(1, right_forward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Treads turned " + str(radius*3.6) + " degrees left.\n")
    pass


def setup():
    # Motor initialization
    global pwm_A, pwm_B
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(Motor_A_EN, GPIO.OUT)
    GPIO.setup(Motor_B_EN, GPIO.OUT)
    GPIO.setup(Motor_A_Pin1, GPIO.OUT)
    GPIO.setup(Motor_A_Pin2, GPIO.OUT)
    GPIO.setup(Motor_B_Pin1, GPIO.OUT)
    GPIO.setup(Motor_B_Pin2, GPIO.OUT)

    _motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        pass


def _motorStop():
    # Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)


def _motorRight(status, direction, speed):  # Motor 2 positive and negative rotation
    if status == 0:  # stop
        GPIO.output(Motor_B_Pin1, GPIO.LOW)
        GPIO.output(Motor_B_Pin2, GPIO.LOW)
        GPIO.output(Motor_B_EN, GPIO.LOW)
    else:
        if direction == Dir_backward:
            GPIO.output(Motor_B_Pin1, GPIO.HIGH)
            GPIO.output(Motor_B_Pin2, GPIO.LOW)
            pwm_B.start(100)
            pwm_B.ChangeDutyCycle(speed)
        elif direction == Dir_forward:
            GPIO.output(Motor_B_Pin1, GPIO.LOW)
            GPIO.output(Motor_B_Pin2, GPIO.HIGH)
            pwm_B.start(0)
            pwm_B.ChangeDutyCycle(speed)


def _motorLeft(status, direction, speed):  # Motor 1 positive and negative rotation
    if status == 0:  # stop
        GPIO.output(Motor_A_Pin1, GPIO.LOW)
        GPIO.output(Motor_A_Pin2, GPIO.LOW)
        GPIO.output(Motor_A_EN, GPIO.LOW)
    else:
        if direction == Dir_forward:  #
            GPIO.output(Motor_A_Pin1, GPIO.HIGH)
            GPIO.output(Motor_A_Pin2, GPIO.LOW)
            pwm_A.start(100)
            pwm_A.ChangeDutyCycle(speed)
        elif direction == Dir_backward:
            GPIO.output(Motor_A_Pin1, GPIO.LOW)
            GPIO.output(Motor_A_Pin2, GPIO.HIGH)
            pwm_A.start(0)
            pwm_A.ChangeDutyCycle(speed)
    return direction


def destroy():
    _motorStop()
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':

    forward = {"angle": 0,
               "distance": 1.0
               }

    backward = {"angle": 180,
                "distance": 1.0
                }

    left = {"angle": 270,
            "distance": 1.0
            }

    right = {"angle": 90,
             "distance": 1.0
             }

    # instructions = dict(treads=[forward, backward, left, right])

    instructions = dict(treads=[forward])

    try:
        setup()
        execute(instructions)
        destroy()
    except Exception as e:
        print("Tread exception: %s", e)
        destroy()
