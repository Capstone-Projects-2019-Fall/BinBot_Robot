"""
BinBot Tread module to provide control interface to robot kit's mechanical tread components.

Author: Sean Reddington
Date: 2019/11/8

TODO Check that left and right are mixed up


"""

import time
import RPi.GPIO as GPIO  # Linux required!


# motor_EN_A: Pin7  |  motor_EN_B: Pin11
# motor_A:  Pin8,Pin10    |  motor_B: Pin13,Pin12

Motor_A_EN = 4
Motor_B_EN = 17

Motor_A_Pin1 = 14
Motor_A_Pin2 = 15
Motor_B_Pin1 = 27
Motor_B_Pin2 = 18

Dir_forward = 0
Dir_backward = 1

left_forward = 0
left_backward = 1

right_forward = 0
right_backward = 1

pwn_A = 0
pwm_B = 0


def execute(instructions):
    for e in instructions["treads"]:
        angle = e["angle"]
        dist = e["distance"]
        speed = 100
        radius = angle / 360

        if angle == 0 or angle == 360:
            print("forward")
            motor_left(1, left_forward, speed)
            motor_right(1, right_forward, speed)
            time.sleep(dist)
            motorStop()
        elif angle == 180:
            print("backward")
            motor_left(1, left_backward, speed)
            motor_right(1, right_backward, speed)
            time.sleep(dist)
            motorStop()
        elif 0 < angle < 180:
            print("right")
            motor_left(1, left_forward, speed)
            motor_right(0, right_backward, int(speed*radius))
            time.sleep(dist)
            motorStop()
        elif 180 < angle < 360:
            print("left")
            radius -= 180
            motor_left(0, left_backward, int(speed*radius))
            motor_right(1, right_forward, speed)
            time.sleep(dist)
            motorStop()
        else:
            print("invalid angle")


def turn(angle):
    print("Treads turned " + str(angle) + " degrees.")


def forward(distance):
    print("Moved " + str(distance) + " meters forward.")


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

    motorStop()
    try:
        pwm_A = GPIO.PWM(Motor_A_EN, 1000)
        pwm_B = GPIO.PWM(Motor_B_EN, 1000)
    except:
        pass


def motorStop():
    # Motor stops
    GPIO.output(Motor_A_Pin1, GPIO.LOW)
    GPIO.output(Motor_A_Pin2, GPIO.LOW)
    GPIO.output(Motor_B_Pin1, GPIO.LOW)
    GPIO.output(Motor_B_Pin2, GPIO.LOW)
    GPIO.output(Motor_A_EN, GPIO.LOW)
    GPIO.output(Motor_B_EN, GPIO.LOW)


def motor_right(status, direction, speed):  # Motor 2 positive and negative rotation
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


def motor_left(status, direction, speed):  # Motor 1 positive and negative rotation
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
    motorStop()
    GPIO.cleanup()  # Release resource


if __name__ == '__main__':
    try:
        setup()

    except KeyboardInterrupt:
        destroy()
