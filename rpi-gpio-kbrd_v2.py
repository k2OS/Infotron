""" rpi-gpio-kbrd.py by Chris Swan 9 Aug 2012
GPIO Keyboard driver for Raspberry Pi for use with 80s 5 switch joysticks
*** This did not work with AdvMAME - failed attempt - may be useful for another project
based on python-uinput/examples/keyboard.py by tuomasjjrasanen
https://github.com/tuomasjjrasanen/python-uinput/blob/master/examples/keyboard.py
requires uinput kernel module (sudo modprobe uinput)
requires python-uinput (git clone https://github.com/tuomasjjrasanen/python-uinput)
requires (from http://pypi.python.org/pypi/RPi.GPIO/0.3.1a)
for detailed usage see http://blog.thestateofme.com/2012/08/10/raspberry-pi-gpio-joystick/
"""

import uinput
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN,pull_up_down=GPIO.PUD_UP)
#GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(7, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#events = (uinput.KEY_P,uinput.KEY_H,uinput.KEY_L,uinput.KEY_F,uinput.KEY_A)
events = (uinput.KEY_P,)

device = uinput.Device(events)

fire = True
up = True
down = True
left = True
right = True

while True:
 # if (not fire) and (not GPIO.input(7)):  # Fire button pressed
 #   fire = True
 #   device.emit(uinput.KEY_LEFTCTRL, 1) # Press Left Ctrl key
 # if fire and GPIO.input(7):  # Fire button released
 #   fire = False
 #   device.emit(uinput.KEY_LEFTCTRL, 0) # Release Left Ctrl key

  if (not up) and (not GPIO.input(11)):  # Up button pressed
    up = True
    device.emit(uinput.KEY_P, 1) # Press Up key
  if up and GPIO.input(11):  # Up button released
    up = False
    device.emit(uinput.KEY_P, 0) # Release Up key

#  if (not down) and (not GPIO.input(13)):  # Down button pressed
#    down = True
#    device.emit(uinput.KEY_DOWN, 1) # Press Down key
#  if down and GPIO.input(13):  # Down button released
#    down = False
#    device.emit(uinput.KEY_DOWN, 0) # Release Down key

#  if (not left) and (not GPIO.input(15)):  # Left button pressed
#    left = True
#    device.emit(uinput.KEY_LEFT, 1) # Press Left key
#  if left and GPIO.input(15):  # Left button released
#    left = False
#    device.emit(uinput.KEY_LEFT, 0) # Release Left key

