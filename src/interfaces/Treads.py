"""
BinBot Tread module to provide control interface to robot kit's mechanical tread components.

Author: Sean Reddington
Date: 2019/11/8

TODO Check that left and right are mixed up

"""

import time
import RPi.GPIO as GPIO  # Linux required!
test = False
# test = True

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
speed = 100     # Speed at which the treads move


def executeTreadInstruction(instruction):
    angle = instruction["angle"]
    distance = instruction["distance"]

    if angle == 0 or angle == 360:
        print("Moving " + str(distance * 10) + " cm forward.")
        _forward(distance, speed)

    elif angle == 180:
        print("Moving " + str(distance*10) + " cm backward.")
        _backward(distance, speed)

    elif 0 < angle < 180:
        print("Treads turning " + str(angle) + " degrees right.")
        turn_scale = angle * (2 / 3) * 0.01
        _rightTurn(distance, speed, int(speed * turn_scale))

    elif 180 < angle < 360:
        angle -= 180
        print("Treads turning " + str(angle) + " degrees left.")
        turn_scale = angle* (2 / 3) * 0.01
        _leftTurn(distance, speed, int(speed * turn_scale))
    else:
        print("invalid angle")
        _motorStop()
        raise

    time.sleep(1)
    _motorStop()


def test_executeTreadInstruction(instruction):
    angle = instruction["angle"]
    distance = instruction["distance"]

    if angle == 0 or angle == 360:
        print("Moving " + str(distance * 10) + " cm forward.")
        print(f"Distance: {distance} -- speed: {speed}")

    elif angle == 180:
        print("Moving " + str(distance*10) + " cm backward.")
        print(f"Distance: {distance} -- speed: {speed}")

    elif 0 < angle < 180:
        print("Treads turning " + str(angle) + " degrees right.")
        turn_scale = angle * (2 / 3) * 0.01
        print(f"Distance: {distance} -- speed: {speed} -- radius: {int(speed * turn_scale)}")

    elif 180 < angle < 360:
        angle -= 180
        print("Treads turning " + str(angle) + " degrees left.")
        turn_scale = angle* (2 / 3) * 0.01
        print(f"Distance: {distance} -- speed: {speed} -- radius: {int(speed * turn_scale)}")
    else:
        print("invalid angle")
        raise

    time.sleep(1)


def _forward(distance, speed):
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_forward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Moved " + str(distance*10) + " cm forward.")


def _backward(distance, speed):
    _motorLeft(1, left_backward, speed)
    _motorRight(1, right_backward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Moved " + str(distance*10) + " cm backward.")


def _rightTurn(distance, speed, radius):
    _motorLeft(1, left_forward, speed)
    _motorRight(1, right_backward, radius)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Treads turned " + str(radius*3.6) + " degrees right.")
    pass


def _leftTurn(distance, speed, radius):
    _motorLeft(1, left_backward, radius)
    _motorRight(1, right_forward, speed)
    time.sleep(distance * d_scale)
    _motorStop()
    print("Treads turned " + str(radius*3.6) + " degrees left.")
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

    # test each
    # instructions = dict(treads=[forward, backward, left, right])

    # square
    # instructions = dict(treads=[forward, right, forward, right, forward])

    # random
    # instructions = dict(treads=[forward, right, right, forward, left, left, forward, backward])

    # eight point patrol
    instructions = dict(treads=[
            {"angle": 0, "distance": 1.0},    # move forward 10 cm
            {"angle": 45, "distance": 1.0},   # turn right 45 degrees 7 times
            {"angle": 45, "distance": 1.0},
            {"angle": 45, "distance": 1.0},
            {"angle": 45, "distance": 1.0},
            {"angle": 45, "distance": 1.0},
            {"angle": 45, "distance": 1.0},
            {"angle": 180, "distance": 1.0},  # move backwards 10 cm
        ]
    )

    if test is True:
        for movement in instructions["treads"]:
            print("\ncaptured photo")
            test_executeTreadInstruction(movement)
    else:
        try:
            setup()
            for movement in instructions["treads"]:
                print("\ncaptured photo")
                executeTreadInstruction(movement)
            destroy()
        except Exception as e:
            print("Tread exception: %s", e)
            destroy()
