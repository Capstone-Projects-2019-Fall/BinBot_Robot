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


def hand(command): ## Control the arm movements in and out
    if command == 'in':
        pwm.set_pwm(13, 0, L13_ST3)
        pwm.set_pwm(12, 0, L12_ST4)
        time.sleep(0.5)
        pwm.set_pwm(13, 0, L13_ST2)
        pwm.set_pwm(12, 0, L12_ST2)
    elif command == 'out':
        pwm.set_pwm(12, 0, L12_ST1)
        pwm.set_pwm(13, 0, L13_ST1)

