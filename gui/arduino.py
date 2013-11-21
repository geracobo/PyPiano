import serial

import time

import thread
from Queue import Queue



class Arduino():
	# We receive information sent from the arduino on this queue.
	queue_in = Queue()
	# We send information to the arduino on this queue.
	queue_out = Queue()
	def __init__(self):
		
		self.serial = serial.Serial('/dev/ttyACM0', 9600)
