#!/usr/bin/python
#
# roomSleep_reset.py
#
# Create by Jin
#

import sys
import sharedFunc

def roomSleepReset():
	"This resets roomSleep to -1."
	# -1 means "no for the first time." 0 means "no subsequently"
	#now = datetime.datetime.now()
	#if (now.hour >= 10) and (now.hour <= 20):
	
	sharedFunc.valSave(-1,sys.path[0]+"/data/roomSleep.dat")
	return
	
roomSleepReset()