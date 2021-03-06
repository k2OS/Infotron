# -*- coding: UTF-8 -*-

""" 
Handles input from huge buttons attached to GPIO-pins on the Infotron RPi
More details on the project here: https://labitat.dk/wiki/Infotron

based on rpi-gpio-kbrd.py by Chris Swan 9 Aug 2012
requires uinput kernel module (sudo modprobe uinput)
requires python-uinput (git clone https://github.com/tuomasjjrasanen/python-uinput)
requires RPI.GIO (from http://pypi.python.org/pypi/RPi.GPIO/0.3.1a)

DESCRIPTION
- master timer needed to control if the monítor should be turned off (say.. 2 minutes after inactivity)
  - when timeout is reached, send key event to JS to reset to default slide/screen
- back/forwards 'buttons' to 'navigate' (captured by JS - turns monitor on as well and navigates current slidehow)
 - on/toggle button to turn on the monitor and then control which slideshow is viewed (captured by JS)
 - one output to control a relay (for turning monitor on and off) - set to pin 12 (board-mode) for now 
 - maybe an additional output to control a little light.. (monitor etc. could be turned on/off with a single common output)

Pins are taken from here: 
http://www.hobbytronics.co.uk/image/data/tutorial/raspberry-pi/gpio-pinout.jpg

"""

try:
	import uinput
	import time
	import RPi.GPIO as GPIO


	# pin definitions (BOARD mode)
	# 18+22 - power, outpout ( two relays to break both sides of the cable)
	# 7  - input
	# 11 - input
	# 13 - input 
	# 15 - input - not used for now

	# set which mode we want to talk to the board in (BOARD or BCM as far as I remember)
	GPIO.setmode(GPIO.BOARD)

	#which pins do we want to listen to/send events to - and which mode - remember to update 'events = ' below
	#we are using Pullup, so pins have to be pulled down for 'input'
	# input pins
	GPIO.setup(7,GPIO.IN,pull_up_down=GPIO.PUD_UP)
	GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_UP)
	GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_UP)

	# output pins
	# pin 18+22 is used to turn on/off monitor - default on for 2 minutes
	GPIO.setup(18,GPIO.OUT) 
	GPIO.output(18, GPIO.HIGH)
	GPIO.setup(22,GPIO.OUT) 
	GPIO.output(22, GPIO.HIGH)

	# remember to update this list with events we want to be able to flag up and down - remember ',' at the end
	# P, LEFT and RIGHT are used to navigate slides. They all turn on the monitor as well. 
	# T is for 'Timeout' and is a key sent to JS to tell that the timeout has been reached and that the slideshow should be reset to 
	# standard.
	events = (
		uinput.KEY_P,
		uinput.KEY_T,
		uinput.KEY_LEFT,
		uinput.KEY_RIGHT,
	)

	device = uinput.Device(events)

	# named variables to keep track of debounce
	# on/toggle-button (Power/Program)
	power = True 
	# navigation-buttons
	left = True
	right = True

	# master timer - time in seconds before monitor is turned off and JS told to reset to default slide
	# default should be 7200 seconds
	timeout = 60
	lastupdate = time.time()
	# is the power on or off - 0 = 0ff, 1 = on
	powerstatus = 1


	while True:
	 # if (not fire) and (not GPIO.input(7)):  # Fire button pressed
	 #   fire = True
	 #   device.emit(uinput.KEY_LEFTCTRL, 1) # Press Left Ctrl key
	 # if fire and GPIO.input(7):  # Fire button released
	 #   fire = False
	 #   device.emit(uinput.KEY_LEFTCTRL, 0) # Release Left Ctrl key
	  # test if timeout has been reached
	  if ((time.time() - lastupdate > timeout) and powerstatus):
	    #print "timeout reached"
	    powerstatus = 0
	    # send T to JS
	    device.emit(uinput.KEY_T, 1) # Send Timeout-message to JS
	    device.emit(uinput.KEY_T, 0) # Send Timeout-message to JS
	    # and turn off the display
	    GPIO.output(18,GPIO.LOW)
	    GPIO.output(22,GPIO.LOW)

	  # what happens when we press a button..
	  # power button
	  if (not power) and (not GPIO.input(7)):  # power/program button pressed
	    power = True
	    lastupdate = time.time()
	    device.emit(uinput.KEY_P, 1) # power pressed - program will be changed by JS if necessary
	    # power on the display
	    GPIO.output(18,GPIO.HIGH)
	    GPIO.output(22,GPIO.HIGH)
	    powerstatus = 1
	  if power and GPIO.input(7):  # power button released
	    power = False
	    lastupdate = time.time()
	    device.emit(uinput.KEY_P, 0) # Release P key

	  # LEFT button
	  if (not left) and (not GPIO.input(11)):  # Left button pressed
	    left = True
	    lastupdate = time.time()
	    device.emit(uinput.KEY_LEFT, 1) # Press Left key
	    GPIO.output(18,GPIO.HIGH)
	    GPIO.output(22,GPIO.HIGH)
	    powerstatus = 1
	  if left and GPIO.input(11):  # Left button released
	    left = False
	    lastupdate = time.time()
	    device.emit(uinput.KEY_LEFT, 0) # Release Left key

	  # RIGHT button
	  if (not right) and (not GPIO.input(13)):  # Right button pressed
	    right = True
	    lastupdate = time.time()
	    device.emit(uinput.KEY_RIGHT, 1) # Press Left key
	    GPIO.output(18,GPIO.HIGH)
	    GPIO.output(22,GPIO.HIGH)
	    powerstatus = 1
	  if right and GPIO.input(13):  # Right button released
	    right = False
	    lastupdate = time.time()
	    device.emit(uinput.KEY_RIGHT, 0) # Release Right key
	  time.sleep(0.01) # this ensures python doesn't eat all of the CPU
except KeyboardInterrupt:
   GPIO.cleanup()
