#!/usr/bin/python
#
# switchRegulator.py
#
# Main script to contain all code that talk to other swtihces
# Create by Jin
#

import sys
#import datetime
import requests
import wol
import logging
from logging.handlers import RotatingFileHandler
logging.basicConfig(level=logging.INFO)

logName = 'switchRegulator'
def setParentName(str):
	global logName
	logName = str
	return

bedroomLamp_logger = logging.getLogger(__name__)
bedroomLamp_logFile = sys.path[0]+'/logs/bedLamp.log'
bedroomLamp_handler = RotatingFileHandler(bedroomLamp_logFile, mode='a', maxBytes=0.25*1024*1024, backupCount=2, encoding=None, delay=0)
#bedroomLamp_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
bedroomLamp_format = logging.Formatter('%(asctime)s - %(message)s')
bedroomLamp_handler.setFormatter(bedroomLamp_format)
bedroomLamp_logger.addHandler(bedroomLamp_handler)
bedroomLamp_logger.setLevel(logging.INFO)

try:
	bedroomLamp_last
except NameError:
	bedroomLamp_last = 'none'

def bedroomLamp(mode):
	"This sends a command to the bedroom lamp."
	global bedroomLamp_last
	
#if (bedroomLamp_last != mode):
	bedroomLamp_last = mode
	print('Lights: '+mode)
	attempt=0
	while (attempt < 10):
		attempt+=1
		try:
			r = requests.get("http://192.168.1.76/cgi-bin/json.cgi?set="+mode)
			#bedroomLamp_logger.info(logName+' setting Bedroom Lamp as '+mode)
			break
		except requests.exceptions.RequestException as e:    # This is the correct syntax
			print e
		
		if (attempt == 10):
			bedroomLamp_logger.info('ERROR: '+logName+' unable to set Bedroom Lamp as '+mode)
			break
#else:
#	print('Lights: Unchanged')
	
	return

def bedroomFan(mode):
	"This sends a command to the bedroom fan."
	
	print('Fan: '+mode)
	attempt=0
	while (attempt < 10):
		attempt+=1
		try:
			r = requests.get("http://192.168.1.77/cgi-bin/json.cgi?set="+mode)
			#bedroomLamp_logger.info(logName+' setting Bedroom Lamp as '+mode)
			break
		except requests.exceptions.RequestException as e:    # This is the correct syntax
			print e
		
		#if (attempt == 10):
			#bedroomLamp_logger.info(logName+' unable to set Bedroom Lamp as '+mode)\
	return
	
def bedroomPc(mode):
	"This sends a command to the pc."
	if (mode == "sleep"):
		attempt=0
		while (attempt < 10):
			attempt+=1
			try:
				r = requests.get("http://jin:jineius@192.168.1.10:9090/?System.Sleep")
				break
			except requests.exceptions.RequestException as e:    # This is the correct syntax
				print e
			
			if (attempt == 10):
				break
			else:
				sharedFunc.valSave(-1,sys.path[0]+'/data/presencePc.dat')
	elif (mode == "wake"):
		wol.jinPC();
	return
	