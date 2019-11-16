'''
Arm class to control arm movements such as move out/ move in
close claw / open claw

Author: Jose Silva
Date: 2019/11/14
'''

from __future__ import division
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685

pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


def hand(command):  # Control the arm movements in and out
    if command == 'in':
        pwm.set_pwm(13, 0, L13_ST3)
        pwm.set_pwm(12, 0, L12_ST4)
        time.sleep(0.5)
        pwm.set_pwm(13, 0, L13_ST2)
        pwm.set_pwm(12, 0, L12_ST2)
    elif command == 'out':
        pwm.set_pwm(12, 0, L12_ST1)
        pwm.set_pwm(13, 0, L13_ST1)


def hand_pos(pos):  # Believe to control the claw rotation
    if pos <= 4:
        pwm.set_pwm(12, 0, L12_ST1 - 30 * pos)
        pwm.set_pwm(13, 0, L13_ST1 - 30 * pos)
    else:
        pwm.set_pwm(12, 0, (L12_ST1 - 24 * pos))
        pwm.set_pwm(13, 0, L13_ST3 - 6 * (pos - 4))


def catch(pos):
    pwm.set_pwm(15, 0, L15_ST2 + 10 * pos)


def clean_all():
    pwm.set_pwm(0, 0, 0)
    pwm.set_pwm(1, 0, 0)
    pwm.set_pwm(2, 0, 0)
    pwm.set_pwm(3, 0, 0)
    pwm.set_pwm(4, 0, 0)
    pwm.set_pwm(5, 0, 0)
    pwm.set_pwm(6, 0, 0)
    pwm.set_pwm(7, 0, 0)
    pwm.set_pwm(8, 0, 0)
    pwm.set_pwm(9, 0, 0)
    pwm.set_pwm(10, 0, 0)
    pwm.set_pwm(11, 0, 0)
    pwm.set_pwm(12, 0, 0)
    pwm.set_pwm(13, 0, 0)
    pwm.set_pwm(14, 0, 0)
    pwm.set_pwm(15, 0, 0)


if __name__ == '__main__':
    try:
        hand('in')
        time.sleep(5)
        hand('in')
        hand('in')

    except KeyboardInterrupt:
        clean_all()
