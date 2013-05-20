# -*- coding: UTF-8 -*-

""" 
	Turns on the monitor after boot
	This should be done by the uinput-script later on (monday...)
"""

try:
#	import uinput
#	import time
	import RPi.GPIO as GPIO


	# pin definitions (BOARD mode)
	# 18+22 - power, outpout ( two relays to break both sides of the cable)

	# set which mode we want to talk to the board in (BOARD or BCM as far as I remember)
	GPIO.setmode(GPIO.BOARD)

	# output pins
	# pin 18+22 is used to turn on/off monitor - default off
	GPIO.setup(18,GPIO.OUT) 
	GPIO.output(18, GPIO.HIGH)
	GPIO.setup(22,GPIO.OUT) 
	GPIO.output(22, GPIO.HIGH)
	print "relays on"
except KeyboardInterrupt: 
   print "Good bye"
   GPIO.cleanup()
