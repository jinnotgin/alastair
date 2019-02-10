#!/usr/bin/python
#
# dataCompiler.py
#
# Create by Jin
#

import sys
import os
import json
import time
import sharedFunc
import sensorLight
import sensorTemp

# path for main/all settings
#outFilePath = sys.path[0]+"/data/all.json"
jsonFilePath = '/run/shm/alastairData.json'
motionTimeout = 300

def sum_digits(digit):
    return sum(int(x) for x in digit if x.isdigit())

def getValue(sItem):
	"This returns the value of any setting."
	inFilePath = sys.path[0]+"/data/"+sItem+".dat"
	
	dataValue = 0
	if (sItem == 'lightLevel'):
		dataValue = float(sensorLight.readLight())
	elif (os.path.isfile(inFilePath)):
		# check if file is being written (size 0), give it some time
		attempt=0
		while (attempt < 9 & os.stat(inFilePath).st_size == 0):
			attempt+=1
			if (attempt <= 9):
				time.sleep(0.1)
		if (attempt == 10):
			dataValue = -1
		else:
			inFile = open(inFilePath, 'r')
			if (sItem == "presenceMotion"):
				dataValue = float(inFile.read())
				if (time.time() - dataValue <= motionTimeout):
					dataValue = 1
				else:
					dataValue = 0
			elif (sItem == "presenceWifi"):
				dataValue = str(inFile.read())
				if sum_digits(dataValue) == 0:
					# sum of all digits are 0
					dataValue = 0
				elif str(dataValue[-2:]) == "01":
					# last 2 digits is 01, just got home
					dataValue = 9
				else:
					dataValue = 1
			else:
				dataValue = int(inFile.read())
			inFile.close()
		
	return dataValue

def toDict():
	"This compiles all data into a python list format."
	
	sharedFunc.sPrint("Compile: Creating data dictionary...")
	# compile individual module data to one big file
	data = {}
	#dataToCheck = ["presenceBt","presencePc","presenceMotion","presenceWifi","roomSleep","pcAwake","lightLevel"]
	dataToCheck = ["presenceBt","presencePc","presenceMotion","presenceWifi","roomSleep","keepPcAwake","sensorsMode"]
	for sItem in dataToCheck:
		data[sItem] = getValue(sItem)

	# set presence value (only for BT and PC)
	if (data['presenceBt'] == 1) or (data['presencePc'] == 1):
		if (data['presenceBt'] == 1) and (data['presencePc'] == 1):
			data['presence'] = int(9)
		elif (data['presencePc'] == 1):
			data['presence'] = int(2)
		elif (data['presenceBt'] == 1):
			data['presence'] = int(1)
	else:
		data['presence'] = int(0)
	
	# light sensor
	data['lightLevel'] = float(sensorLight.readLight())
	
	# temp sensor
	data['temperature'] = float(sensorTemp.read_temp())
	
	return data
	
def exportJson():
	"This compiles all data into json format."
	
	sharedFunc.sPrint("\nType: exportJson")
	
	data = toDict()
	
	# save main/all settings to file
	dataJson = json.dumps(data);
	sharedFunc.sPrint("Data: " + dataJson)
	outFile = open(jsonFilePath, 'w')
	outFile.write(dataJson)
	outFile.close()
	
	sharedFunc.sPrint("Export: "+jsonFilePath)
	
	return

if __name__=="__main__":
	if "-silent" in sys.argv:
		sharedFunc.sPrint_silent = 1
	if "-jsonExport" in sys.argv:
		while True :
			exportJson()
			sharedFunc.sPrint("\n[*] Sleeping for 5 seconds")
			time.sleep(5)
	else:
		print(toDict())