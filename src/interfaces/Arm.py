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
        pwm.set_pwm(13, 0, 75)
        pwm.set_pwm(12, 0, 50)
        time.sleep(3)
        pwm.set_pwm(13, 0, 200)
        pwm.set_pwm(12, 0, 150)
    elif command == 'out':
        #pwm.set_pwm(12, 0, 130)
        #pwm.set_pwm(13, 0, 129)
        #time.sleep(1)
        #pwm.set_pwm(12, 0, 400)
        #pwm.set_pwm(13, 0, 399)
        #time.sleep(1)
        #pwm.set_pwm(12, 0, 50)
        #pwm.set_pwm(13, 0, 85)
        #time.sleep(1)
        pwm.set_pwm(13, 0, 100)
        pwm.set_pwm(13, 0, 99)
        time.sleep(1)
       # pwm.set_pwm(12, 0, 327)
       # pwm.set_pwm(13, 0, 231)
       # time.sleep(1)
        pwm.set_pwm(12, 0, 400)
        pwm.set_pwm(13, 0, 399)
      # time.sleep(1)
        pwm.set_pwm(13, 0, 100)
        time.sleep(10)


def hand_pos(pos):  # Believe to control the claw rotation
    if pos <= 4:
        pwm.set_pwm(12, 0, 430 - 30 * pos)
        pwm.set_pwm(13, 0, 429 - 30 * pos)
    else:
        pwm.set_pwm(12, 0, (430 - 24 * pos))
        pwm.set_pwm(13, 0, 298 - 6 * (pos - 4))


def catch(pos):
    pwm.set_pwm(15, 0, 194 + 10 * pos)


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
        pos_input = 0
        OUT = 1
        while 1:
            a = input()

            if OUT == 1:
                if pos_input < 13:
                    pos_input += 1
                else:
                    hand('out')
                    print('MAX')
                    OUT = 0
            else:
                if pos_input > 1:
                    pos_input -= 1
                else:
                    print('MIN')
                    OUT = 1
            catch(pos_input)
            print(pos_input)

            pass
    except KeyboardInterrupt:
        clean_all()
