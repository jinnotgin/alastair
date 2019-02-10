#!/usr/bin/python
#
# mainLoop.py
#
# Loops main.py
# Create by Jin
#

import sys
import time
import sharedFunc
import rulesProcessor
import switchRegulator

switchRegulator.setParentName("rulesProcessor (Loop)")
rulesProcessor.callerName = "rulesProcessor (Loop)"
triggerLight_last = 'none';

# silent detection
if len(sys.argv) > 1 and sys.argv[1] == "-silent":
	sharedFunc.sPrint_silent = 1

try:
	while True :
		rulesProcessor.checkAll()
		sharedFunc.sPrint("\n[*] Sleeping for 120 seconds")
		time.sleep(120)
	
except KeyboardInterrupt:
	sharedFunc.sPrint("\nQuit")
