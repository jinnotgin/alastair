#!/usr/bin/env python
import json
import urllib2
import sys

def sPrint(str):
	global sPrint_silent
	
	try:
		sPrint_silent
	except NameError:
		print(str)
	else:
		if sPrint_silent != 1:
			print(str)
	return
	
def valSave(valToSave,filePath):
	outFile = open(filePath, 'w')
	outFile.write(str(valToSave))
	outFile.close()
	return
	
def pushbullet(message):
	token = "YtymmlWfUVlATvPbHP1UW8u1MrDqlNdU"
	recepient = "udqhCsjAnpRXKnLg"
	
	jdata = json.dumps({"device_iden": recepient, "type": "note", "title": "Alastair", "body": message})
	request = urllib2.Request("https://api.pushbullet.com/v2/pushes", headers={"Authorization": "Bearer %s" % (token), "Content-Type": "application/json"})

	contents = urllib2.urlopen(request, jdata).read()
	return
	
if __name__=="__main__" and len(sys.argv) > 2 and sys.argv[1] == "pushbullet":
	pushbullet(sys.argv[2])