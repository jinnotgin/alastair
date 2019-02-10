#!/usr/bin/python
#
# rules.py
#
# Main script to determine various automation decisions
# Create by Jin
#

import sys
import time
#import datetime
import dataCompiler
import switchRegulator
import sharedFunc
import logging
import pickle
from logging.handlers import RotatingFileHandler

# USER VARIABLES
lightThreshold = (850,950)
logFilePath = sys.path[0]+'/logs/rulesProcessor.log'

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
loggerHandler = RotatingFileHandler(logFilePath, mode='a', maxBytes=0.25*1024*1024, backupCount=2, encoding=None, delay=0)
#loggerFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerFormat = logging.Formatter('%(asctime)s - %(message)s')
loggerHandler.setFormatter(loggerFormat)
logger.addHandler(loggerHandler)
logger.setLevel(logging.INFO)

# system variables
callerName = "rulesProcessor"
	
## AUTOMATION FUNCTIONS
def dataExist(keysNeeded,data,allNeeded=1):
	"This checks if needed data(s) info is in the dictionary."
	
	# if string, convert keysNeeded to a tuple
	if type(data) == str:
		data = (data)
		
	result = 1
	keysMissing = 0
	
	for iKey in keysNeeded:
		if (data.has_key(iKey) == 0):
			keysMissing += 1
			if (allNeeded == 1):
				result = 0
				break

	if (allNeeded == 0) and (keysMissing == len(keysNeeded)):
		result = 0
		
	return result

def dictSave(obj, name ):
    with open(sys.path[0]+'/data/'+name+'.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def dictLoad(name ):
    with open(sys.path[0]+'/data/'+name+'.pkl', 'rb') as f:
        return pickle.load(f)
	
def checkAll(data={}):
	"This checks data against rules."
	sharedFunc.sPrint("\nType: checkAll")
	sharedFunc.sPrint("Time: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
	
	# check if data dictionary has any keys at all
	if (any(data) == False):
		data = dataCompiler.toDict()
	else:
		# prepare essential data
		data["sensorsMode"] = dataCompiler.getValue("sensorsMode")
		data["lightLevel"] = dataCompiler.getValue("lightLevel")
		data["roomSleep"] = dataCompiler.getValue("roomSleep")
		data["presenceMotion"] = dataCompiler.getValue("presenceMotion")
		data["presenceWifi"] = dataCompiler.getValue("presenceWifi")
	
	sharedFunc.sPrint("Data: "+str(data))
		
	# AUTOMATION RULES
	resultStr = ""
	sharedFunc.sPrint("Check: All Rules")
	
	# disable if sensorsMode is 0
	if (data.get('sensorsMode','NA') == 0):
		# end now
		sharedFunc.sPrint('sesnorMode is 0, all rules bypassed.')
		return
	
	# based on roomSleep 
	if (data['roomSleep'] == 0) or (data['roomSleep'] == -1):
		if (data['lightLevel'] < lightThreshold[0]):
			#resultStr += "Light is below threshold of "+lightThreshold[0]+", "
			if (data.get('presenceMotion',0) == 1):
				sharedFunc.sPrint('Presence: Motion')
				sharedFunc.sPrint('Elapsed: '+str(time.time() - float(data['presenceMotion'])))
				sharedFunc.sPrint('Ambient: Dark')
				switchRegulator.bedroomLamp('on')
				resultStr += "Motion detected recently. Bedroom Lamp = On. "
			elif (data.get('presenceBt','NA') == 0):
				sharedFunc.sPrint('BT: Missing')
				switchRegulator.bedroomLamp('off')
				resultStr += "Missing BT device. Bedroom Lamp = Off. "
			#elif ((data.get('presenceBt',0) == 1) or (data.get('presencePc',0) == 1)):
			elif (data.get('presenceBt',0) == 1 or data.get('presencePc','NA') == 1):
				sharedFunc.sPrint('Presence: BT/PC')
				sharedFunc.sPrint('Ambient: Dark')
				switchRegulator.bedroomLamp('on')
				#resultStr += "presenceBt and/or presencePc is 1. Bedroom Lamp = On."
				resultStr += "Present BT device and/or PC is active. Bedroom Lamp = On. "
				
				# if BT is detected but presenceWifi is still 0, then set presenceWifi as "just home" aka 9
				if (data.get('presenceWifi','NA') == 9) and (data.get('presencePc','NA') == -1):
					switchRegulator.bedroomPc('wake')
		elif (data['lightLevel'] > lightThreshold[1]):
			sharedFunc.sPrint('Ambient: Bright')
			switchRegulator.bedroomLamp('off')
			resultStr += "Light is above threshold of "+str(lightThreshold[1])+". Bedroom Lamp = Off. "
		
		# if roomSleep is set to No for the first time
		if (data['roomSleep'] == -1):
			resultStr += "Resetting roomSleep to 0. "
			sharedFunc.valSave(0,sys.path[0]+'/data/roomSleep.dat')
			if (data['presencePc'] == -1) or (dataCompiler.getValue("presencePc") == -1):
				switchRegulator.bedroomPc('wake')
				resultStr += "Jin's PC = Wake. "
	elif (data['roomSleep'] == 1):
		switchRegulator.bedroomLamp('off')
		resultStr += "Bedroom Lamp = Off. "
		
		if (dataCompiler.getValue("keepPcAwake") == 0) and (dataCompiler.getValue("presencePc") != -1):
			switchRegulator.bedroomPc('sleep')
			resultStr += "Jin's PC = Sleep. "
		
	# (if phone is not at home, in that no BT and no Wifi)
	if (data.get('presenceWifi','NA') == 0) and (data.get('presenceBt','NA') == 0):
		resultStr += "Jin is not currently at home. "
		if (dataCompiler.getValue("presenceHome") == 1):
			sharedFunc.valSave(0,sys.path[0]+'/data/presenceHome.dat')
			sharedFunc.pushbullet("Goodbye Jin! Devices will now be turned off.")
		if (data['roomSleep'] != 0):
			# set roomSleep as 0
			sharedFunc.valSave(0,sys.path[0]+'/data/roomSleep.dat')		
			resultStr += "roomSleep is set to 0. "
		
		if (data.get('presencePc','NA') != -1):
			# turn off PC
			switchRegulator.bedroomPc('sleep')
			resultStr += "Jin's PC = Sleep."
		
	# (if phone just got home)
	if (data.get('presenceWifi','NA') == 9):
		if (dataCompiler.getValue("presenceHome") == 0):
			sharedFunc.valSave(1,sys.path[0]+'/data/presenceHome.dat')
		if (data.get('presencePc','NA') == -1):
			switchRegulator.bedroomPc('wake')
	
	# new code for fan (not optimised, newish)
	if (data.get('presenceBt','NA') == 0):
		switchRegulator.bedroomFan('off')
		resultStr += "Bedroom Fan = Off. "
	elif (data.get('presenceBt','NA') == 1):
		switchRegulator.bedroomFan('on')
		resultStr += "Bedroom Fan = On. "
		
		
	if (resultStr == ""):
		sharedFunc.sPrint('No rules are matched. No action is taken.')
	logger.info(callerName+"'s request using "+str(data)+". "+resultStr)
	return

if __name__=="__main__":
	if "-silent" in sys.argv:
		sharedFunc.sPrint_silent = 1
	if "-loop" in sys.argv:
		switchRegulator.setParentName("rulesProcessor (Loop)")
		callerName = "rulesProcessor (Loop)"
		triggerLight_last = 'none';
		try:
			while True :
				checkAll()
				sharedFunc.sPrint("\n[*] Sleeping for 120 seconds")
				time.sleep(120)
			
		except KeyboardInterrupt:
			sharedFunc.sPrint("\nQuit")
	else:
		checkAll()