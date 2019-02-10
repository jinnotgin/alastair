#!/bin/bash
# one-liner to find current location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Which Interface do you want to check
wlan='wlan0'
# Which address do you want to ping to see if you can connect
pingip='192.168.1.1'

LOG_FILE="$DIR/logs/wifiKeepAlive.log"

NOW1=$(date +"%Y-%m-%d")
NOW2=$(date +"%H:%M:%S,%3N")
NOW="$NOW1 $NOW2"

# Perform the network check and reset if necessary
/bin/ping -c 2 -I $wlan $pingip > /dev/null 2> /dev/null
if [ $? -ge 1 ] ; then
    logger -t $0 "WiFi seems down, restarting."
    echo "$NOW - WiFi seems down, restarting." >> $LOG_FILE
    #ifdown -- force $wlan
    #sleep 5
    #ifup $wlan
    reboot now
else
    logger -t $0 "WiFi seems up."
    echo "$NOW - WiFi seems up." >> $LOG_FILE
fi

# keep last 2000 lines in log
LASTDATA=$(tail -n 2000 $LOG_FILE)
echo "${LASTDATA}" > $LOG_FILE