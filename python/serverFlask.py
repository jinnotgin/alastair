from flask import Flask
import rulesProcessor
import switchRegulator
import sharedFunc
import dataCompiler

sharedFunc.sPrint_silent = 1

def setCaller(phpCaller):	
	switchRegulator.setParentName("PHP ("+phpCaller+")")
	rulesProcessor.callerName = "PHP ("+phpCaller+")"
	dataCompiler.exportJson()
	
setCaller("Unknown")

app = Flask(__name__)

@app.route('/')
def index():
    return "Alastair's Python Flask"

@app.route('/php_roomSleep')
def roomSleep():
	setCaller("roomSleep")
	rulesProcessor.checkAll()
	return 'Caller: roomSleep'
	
@app.route('/php_presencePc')
def presencePc():
	setCaller("presencePc")
	rulesProcessor.checkAll()
	return 'Caller: presencePc'
	
@app.route('/php_onResume')
def onResume():
	setCaller("onResume")
	rulesProcessor.checkAll()
	return 'Caller: onResume'
	
@app.route('/php_sensorsMode')
def sensorsMode():
	setCaller("sensorsMode")
	rulesProcessor.checkAll()
	return 'Caller: sensorsMode'

if __name__ == '__main__':
    app.run(host='0.0.0.0')