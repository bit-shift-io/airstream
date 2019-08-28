#!/usr/bin/env python3

#
# 2016 - Bronson Mathews & Fabian Mathews
#
# http://kropp.ca/tutorials/raspberry-pi-hall-effect-switch/
# https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/hall.py
#
# This will send an email when mains power is not detected for 1 minute
# Then send another email when mains is restored after a minute
#

# Import required libraries
import time
import datetime
from datetime import date

# Import email stuff
import smtplib
from email.mime.text import MIMEText

import voltmeter


# get time
def getTimeStamp():
	timestamp = time.time()
	stamp = datetime.datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')
	return stamp


# read the values on the history array with value smoothing
def readACState(historyArray):
	total = 0
	val = 0
	
	# tally the total of the array
	for val in historyArray:
		total += val
		
	length = len(historyArray)
	percentage = total / length * 100
	
	#print (historyArray)
	#print (percentage)
	
	if percentage < 50:
		return False # low or AC OFF

	# else return
	return True # high or AC on
	
# email function
def sendMail(message, subject):
	print ( message + getTimeStamp() )
	
	sender = 'Teringie-Pi@wfx.net.au'
	receivers = ['justin@wfx.net.au','sfaunt@wfx.net.au','thecookeman@gmail.com','bronsonmathews@gmail.com'] # array of emails
	msg = MIMEText('{}\n{}'.format(message, getTimeStamp()))
	msg['Subject'] = 'Teringie AC Status: {} - {}' .format(subject,getTimeStamp())
	msg['From'] = sender
	msg['To'] = ", ".join(receivers)

	try:
		# Send the message via our own SMTP server.
		s = smtplib.SMTP('localhost')
		s.sendmail(sender, receivers, msg.as_string())
		s.quit()
	except Exception as e:
	   print ('Error: unable to send email')	


# main loop  
def main():
	mHistory = []
	mACState = False # defaults to off
	
	# do some filtering as to avoid a false positive... Mostly high or mostly low...
	while True:
		# sleep for a time
		time.sleep(10)
		
		# read mains state from voltmeter script
		state = False
		try:
			state = voltmeter.mainsStatus()
		except Exception as e:
			print ('Error: unable to read state')
			
		# pre-append 0 or 1 to the array
		mHistory.insert( 0, state)

		# delete elements longer than 6 (~1 minute)
		del mHistory[6:]
		
		# read the current ac state from history
		curACState = readACState(mHistory)
		
		if mACState != curACState:
			if curACState == True:
				sendMail('AC is ON. Chill ', 'ON')
			else:
				sendMail('AC is OFF, Warning: Running on battery backup! ', 'OFF')
				
			mACState = curACState
		

if __name__=="__main__":
	print('Mains running')
	main()
