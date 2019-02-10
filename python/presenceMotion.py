#!/usr/bin/python
#
# pir_1.py
# Detect movement using a PIR module
#
# Author : Matt Hawkins
# Date   : 21/01/2013
#
# Modified by Jin for Room automation project

# Import required Python libraries
import RPi.GPIO as GPIO
import sys
import time
import requests
import presenceBt
import rulesProcessor
import switchRegulator
import sharedFunc
import logging
from logging.handlers import RotatingFileHandler

# USER VARIABLES
outFilePath = sys.path[0]+"/data/presenceMotion.dat"
logFilePath = sys.path[0]+'/logs/presenceMotion.log'

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
loggerHandler = RotatingFileHandler(logFilePath, mode='a', maxBytes=0.25*1024*1024, backupCount=2, encoding=None, delay=0)
#loggerFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerFormat = logging.Formatter('%(asctime)s - %(message)s')
loggerHandler.setFormatter(loggerFormat)
logger.addHandler(loggerHandler)
logger.setLevel(logging.INFO)

# silent detection
if len(sys.argv) > 1 and sys.argv[1] == "-silent":
	sharedFunc.sPrint_silent = 1
	
# setup logging for switchRegulator (to move to rulesProcessor)
switchRegulator.setParentName("presenceMotion")
rulesProcessor.callerName = "presenceMotion"

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO to use on Pi
GPIO_PIR = 7

print "presenceMotion Module (CTRL-C to exit)"
sharedFunc.sPrint("Data: "+outFilePath)

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)      # Echo

Current_State  = 0
Previous_State = 0

try:
	sharedFunc.sPrint("\nWaiting for PIR to settle ...")

	# Loop until PIR output is 0
	while GPIO.input(GPIO_PIR)==1:
		Current_State  = 0    

	sharedFunc.sPrint("\nType: presenceMotion")
	sharedFunc.sPrint("Time: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
	sharedFunc.sPrint("Status: Ready")  
    
	# Loop until users quits with CTRL-C
	while True :
   
		# Read PIR state
		Current_State = GPIO.input(GPIO_PIR)

		if Current_State==1 and Previous_State==0:
			# PIR is triggered
			sharedFunc.sPrint("Result: Motion Detected")
			logger.info("Motion Detected")
			# Record previous state
			Previous_State=1
			# Store data
			timeNow = str(time.time())
			sharedFunc.valSave(timeNow,outFilePath)
			
			# call main.py
			#runpy.run_path(sys.path[0]+"/main.py")
			rulesProcessor.checkAll({"presenceMotion": 1})

			# if fan is off, (move this part to rulesProcessor in the future)
			try:
				r = requests.get("http://192.168.1.77/cgi-bin/json.cgi?get=state")
			except:
				pass
			else:
				if r.json()['state'] == "off":
					presenceBt.checkInstantly = True
					presenceBt.checkBt()
			
			# Wait a while
			sharedFunc.sPrint("\n[*] Sleeping for 20 seconds")
			time.sleep(20)
		elif Current_State==0 and Previous_State==1:
			# PIR has returned to ready state
			# Store data
			#outFile = open(outFilePath, 'w')
			#outFile.write('0')
			#outFile.close()
			
			# Prepare
			sharedFunc.sPrint("\nType: presenceMotion")
			sharedFunc.sPrint("Time: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
			sharedFunc.sPrint("Status: Ready")
			logger.info("Ready")
			Previous_State=0
		  
		# Wait for 10 milliseconds
		time.sleep(0.01)      
      
except KeyboardInterrupt:
	print "\nQuit" 
	# Reset GPIO settings
	GPIO.cleanup()
