#!/usr/bin/python
#
# Create by Jin
#

import sys
#sys.path.insert(0, sys.path[0]) # or: sys.path.insert(0, os.getcwd())
import rulesProcessor
import switchRegulator
import sharedFunc

sharedFunc.sPrint_silent = 1

phpCaller = "Unknown"
if len(sys.argv) > 1:
	phpCaller = sys.argv[1]
	
switchRegulator.setParentName("PHP ("+phpCaller+")")
rulesProcessor.callerName = "PHP ("+phpCaller+")"

rulesProcessor.checkAll()