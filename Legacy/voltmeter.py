#!/usr/bin/env python3

#
# 2016 - Fabian Mathews
#
# Read voltages from the arduino over serial port and dump to file
# This needs to be running constantly in the background to keep the file updating
#
# apt-get install python3
# apt-get install pip3-python (or python3-pip)
# pip3 install setuptools
# pip3 install pyserial

import os
import serial
import json
import sys
import time
from time import time

voltageDividerMagicNumber = 5.66
jsonFileName = 'voltmeter.json'

# True = AC is running
# False = AC off
def mainsStatus():
	try:		
		with open(jsonFileName) as data_file:    
			pinVolData = json.load(data_file)
			return (pinVolData["4"] > 2.0)
	except:
		print ('Unable to read json')
		return false			
		
# Get the estimated battery voltage
def batteryVoltage():
	try:		
		with open(jsonFileName) as data_file:    
			pinVolData = json.load(data_file)
			return (pinVolData["0"] * voltageDividerMagicNumber)
	except:
		print ('Unable to read json')		
		return 0			

if __name__ == '__main__':  
	
	# store time in seconds
	lastTime = time()
	
	if len(sys.argv) == 2 and sys.argv[1] == "battery":
		print(str(batteryVoltage()))
		sys.exit()
		
	if len(sys.argv) == 2 and sys.argv[1] == "mains":
		print(str(mainsStatus()))
		sys.exit()
	
	print("Running Serial Voltmeter")

	try:
		if os.name == 'nt':
			ser = serial.Serial('COM1', 9600)
		else:
			ser = serial.Serial('/dev/ttyUSB0', 9600)
	except e:
		print(e)
		sys.exit()

	while True:
		# readline will block till something appears
		line = ser.readline()
		line = line.strip()
		
		# flush serial buffer
		ser.flush()		

		if len(line) <= 0:
			continue
			
		if time() < (lastTime + 10):
			continue
			
		lastTime = time()
		
		try:
			pinVolData = json.loads(line.decode())
		except:
			continue
		#print(pinVolData)
		
		print("A0\t Vp: {0:0.1f}".format(pinVolData["0"]) + "\tVc: {0:0.1f}".format(pinVolData["0"] * voltageDividerMagicNumber)
			+ "\t| A4\t Vp: {0:0.1f}".format(pinVolData["4"]))
			
		try:			
			with open(jsonFileName, 'w') as outfile:
				json.dump(pinVolData, outfile)
		except:
			print ('Unable to write json')			
			continue	
