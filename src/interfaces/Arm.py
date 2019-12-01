'''
Arm class to control arm movements such as move out/ move in
close claw / open claw

Author: Jose Silva
Date: 2019/11/14
'''

from __future__ import division
import DistanceSensor
import time
import RPi.GPIO as GPIO
import sys
import Adafruit_PCA9685


pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)


def hand(command):  # Control the arm movements in and out
    if command == 'in':
        pwm.set_pwm(13, 0, 75)
        pwm.set_pwm(12, 0, 50)
        time.sleep(3)
        pwm.set_pwm(13, 0, 140)
        pwm.set_pwm(12, 0, 100)
    elif command == 'out':
        pwm.set_pwm(13, 0, 100)
        pwm.set_pwm(13, 0, 99)
        time.sleep(1)
        pwm.set_pwm(12, 0, 400)
        pwm.set_pwm(13, 0, 399)
        pwm.set_pwm(13, 0, 100)
        time.sleep(60)
        pwm.set_pwm(13, 0, 100)
        time.sleep(60)
        pwm.set_pwm(13, 0, 100)


def hand_pos(pos):
    if pos <= 4:
        pwm.set_pwm(12, 0, 430 - 30 * pos)
        pwm.set_pwm(13, 0, 429 - 30 * pos)
    else:
        pwm.set_pwm(12, 0, (430 - 24 * pos))
        pwm.set_pwm(13, 0, 298 - 6 * (pos - 4))

def openClaw(): # Open claw of the robot
    pwm.set_pwm(15, 0, 80)

def catch():  # Close claw of the robot
    pwm.set_pwm(15, 0, 574)


def cir_pos(pos):  # Controls the rotation of the claw
    pwm.set_pwm(14, 0, 350 + 30 * pos)  # pos = 5 to get 90 degree


def cir_back():  # Rotates the claw back to starting position
    pwm.set_pwm(14, 0, 290)

def home():
    pwm.set_pwm(12, 0, 450)
    pwm.set_pwm(13, 0, 399)
    #pwm.set_pwm(13, 0, 100)


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

        home()

       # while 1:
       #     if .10 < DistanceSensor.checkdistance() < .11:
       #         print(DistanceSensor.checkdistance())
       #         openClaw()
       #         time.sleep(1)
       #         hand('in')
       #         time.sleep(1)
       #         catch() # pwm.set_pwm(15, 0, 574)
       #         time.sleep(1)
       #         hand('out')
       #         if
       #     else:
       #         print(DistanceSensor.checkdistance())
       #         print("not in range")
       #     time.sleep(5)

    except KeyboardInterrupt:
        clean_all()
