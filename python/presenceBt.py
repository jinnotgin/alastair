#!/usr/bin/python

# Raspberry Pi Bluetooth In/Out Board or "Who's Home" by prb3333
# http://www.instructables.com/id/Raspberry-Pi-Bluetooth-InOut-Board-or-Whos-Hom/
#
# inoutboard.py
#
# Modified by Jin for Room automation project

import sys
import bluetooth
import time
import rulesProcessor
import switchRegulator
import sharedFunc
import logging
from logging.handlers import RotatingFileHandler

# USER VARIABLES
btMac = "3C:BB:FD:6C:25:32"
btStr = "Jin's S7E"
outFilePath = sys.path[0]+"/data/presenceBt.dat"
motionFilePath = sys.path[0]+"/data/presenceMotion.dat"
logFilePath = sys.path[0]+'/logs/presenceBt.log'

# set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
loggerHandler = RotatingFileHandler(logFilePath, mode='a', maxBytes=0.25*1024*1024, backupCount=2, encoding=None, delay=0)
#loggerFormat = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
loggerFormat = logging.Formatter('%(asctime)s - %(message)s')
loggerHandler.setFormatter(loggerFormat)
logger.addHandler(loggerHandler)
logger.setLevel(logging.INFO)

checkInstantly = False
# silent detection
if len(sys.argv) > 1 and sys.argv[1] == "-silent":
	sharedFunc.sPrint_silent = 1
elif len(sys.argv) > 1 and sys.argv[1] == "-once":
	sharedFunc.sPrint_silent = 1
	checkInstantly = True

# setup logging for switchRegulator (to move to rulesProcessor)
switchRegulator.setParentName("presenceBt")
rulesProcessor.callerName = "presenceBt"

def checkBt():
        print "presenceBt Module (CTRL-C to exit)"
        sharedFunc.sPrint("Data: "+outFilePath) 

        missingNo = 0
        foundNo = 0

        sleepAmt = 20
        try:
                while True:
                        startRulesProcessor = 0
                        sharedFunc.sPrint("\nType: presenceBt") 
                        sharedFunc.sPrint("Time: "+time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime()))
                        sharedFunc.sPrint("Find: " + btStr + " (" + btMac  + ")")

                        try:
                                result = bluetooth.lookup_name(btMac, timeout=3)
                        except:
                                sharedFunc.sPrint("\n[*] Unable to scan. Trying again in 5 seconds.")
                                time.sleep(5)
                        else:
                                resultInt = 0
                                if (result != None):
                                        if (foundNo >= 2 or checkInstantly):
                                                sharedFunc.sPrint("Result: Found")
                                                logger.info("Found")
                                                sleepAmt = 60
                                                resultInt = 1
                                                if (foundNo == 2 or checkInstantly):
                                                        startRulesProcessor = 1
                                                if (foundNo <= 19):
                                                        sleepAmt = 30
                                                        foundNo += 1
                                        else:
                                                sharedFunc.sPrint("Result: Possibly Found")
                                                logger.info("Possibly Found")
                                                sleepAmt = 5
                                                resultInt = -1
                                                missingNo = 0
                                                foundNo += 1
                                else:
                                        if (missingNo >= 4):
                                                sharedFunc.sPrint("Result: Missing")
                                                logger.info("Missing")
                                                sleepAmt = 120
                                                resultInt = 0
                                                
                                                if (missingNo == 4):
														startRulesProcessor = 1
														# if BT is missing, then set motion as (current time - 301 seconds)
														sharedFunc.valSave(str(time.time()-301),motionFilePath)
                                                if (missingNo <= 19):
                                                        sleepAmt = 30
                                                        missingNo += 1
                                        else:
                                                sharedFunc.sPrint("Result: Possibly Missing")
                                                logger.info("Possibly Missing")
                                                sleepAmt = 5
                                                resultInt = -1
                                                foundNo = 0
                                                missingNo += 1
                                
                                if (resultInt != -1): 
                                        sharedFunc.valSave(resultInt,outFilePath)
                                
                                if (startRulesProcessor == 1):
                                        # call main.py
                                        #runpy.run_path(sys.path[0]+"/main.py")
                                        
                                        rulesProcessor.checkAll({"presenceBt": resultInt})
                                        startRulesProcessor = 0
                                
                                if checkInstantly:
                                        break
                                else:
                                        sharedFunc.sPrint("\n[*] Sleeping for "+str(sleepAmt)+" seconds")
                                        time.sleep(sleepAmt)

        except KeyboardInterrupt:
            print "\nQuit"

        return

if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
   checkBt()
