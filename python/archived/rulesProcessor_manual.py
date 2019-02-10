#!/usr/bin/python
#
# Create by Jin
#

import sys
import rulesProcessor
import switchRegulator
import sharedFunc

switchRegulator.setParentName("rulesProcessor (Manual)")
rulesProcessor.callerName = "rulesProcessor (Manual)"

if len(sys.argv) > 1 and sys.argv[1] == "-silent":
	sharedFunc.sPrint_silent = 1

rulesProcessor.checkAll()