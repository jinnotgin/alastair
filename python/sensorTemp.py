import os
import time
import sys

# if not set to default, enable drivers
#os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

temp_sensor = "/sys/bus/w1/devices/28-0415922058ff/w1_slave"

def temp_raw():
    f = open(temp_sensor, 'r')
    lines = f.readlines()
    f.close()
    return lines
	
def read_temp():
    lines = temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw()
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        #temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_c,2)
		
if __name__=="__main__":
	if len(sys.argv) > 1 and sys.argv[1] == "-once":
		print(read_temp())
	else:
		while True:
			print(read_temp())
			time.sleep(1)