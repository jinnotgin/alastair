#!/bin/bash
# one-liner to find current location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# user variables
FINDPHONE=("60:f1:89:1b:3f:82|Jin's S7E|presenceWifi")
FINDPC=("8c:ae:4c:fe:01:94|Jin's PC|presencePc")
PINGPC=("192.168.1.10|Jin's PC|presencePc")
DATA_DIR="$DIR/data/"
LOG_DIR="$DIR/logs/"
#DATA_FILE="$DIR/data/presenceWifi.dat"
#LOG_FILE="$DIR/logs/presenceWifi.log"

# code for logging facility using echo
# exec 3>&1 1>>${LOG_FILE} 2>&1
# TAKE NOTE:
# echo "This is stdout (to logfile only)"
# echo "This is stderr (to logfile only)" 1>&2
# echo "This is the console (fd 3)" 1>&3
# echo "This is both the log and the console" | tee /dev/fd/3

NOW1=$(date +"%Y-%m-%d")
NOW2=$(date +"%H:%M:%S,%3N")
NOW="$NOW1 $NOW2"

# for now, only limit to one ip. but in future, consider expanding.
SCANRESULTS=$(arp-scan --retry=8 --ignoredups 192.168.1.11)
#SCANRESULTS=$(arp-scan 192.168.1.11 -I wlan0 -l -r 10)

for i in "${FINDPHONE[@]}"
do
	:
	IFS='|' read -ra CURRENTDEV <<< "$i"
	
	DATA_FILE="${DATA_DIR}${CURRENTDEV[2]}.dat"
	LOG_FILE="${LOG_DIR}${CURRENTDEV[2]}.log"
	
	CURRENT_DATA=$(<${DATA_FILE})
	CURRENT_DATA_LEN=${#CURRENT_DATA}
		
	if (($CURRENT_DATA_LEN == 5)) 
	then
		ARPOUTPUT=$(echo $CURRENT_DATA|awk '{print substr($0,2,4)}')
	else
		ARPOUTPUT=$CURRENT_DATA
	fi
	
	if echo $SCANRESULTS | grep -q "${CURRENTDEV[0]}"
	then
		ARPOUTPUT+=1
	else
		ARPOUTPUT+=0
	fi
	
	#echo "Found ${CURRENTDEV[1]}"
	echo $ARPOUTPUT > $DATA_FILE
	echo "$NOW - Found ${CURRENTDEV[1]}" >> $LOG_FILE
	#sed -i -e '1i'"$NOW - Found Jin's G4"'\' $LOG_FILE
done

#for i in "${FINDPC[@]}"
for i in "${PINGPC[@]}"
do
	:
	IFS='|' read -ra CURRENTDEV <<< "$i"
	
	DATA_FILE="${DATA_DIR}${CURRENTDEV[2]}.dat"
	LOG_FILE="${LOG_DIR}${CURRENTDEV[2]}.log"
	
	#if echo $SCANRESULTS | grep -q "${CURRENTDEV[0]}"
	ping -c1 "${CURRENTDEV[0]}" 2>/dev/null 1>/dev/null
	if [ "$?" = 0 ]
	then
		#echo "Found ${CURRENTDEV[1]}"
		CURRENT_DATA=$(<${DATA_FILE})
		if [ "$CURRENT_DATA" == "-1" ]
		then
			echo 1 > $DATA_FILE
		fi
		echo "$NOW - Found ${CURRENTDEV[1]}" >> $LOG_FILE
		#sed -i -e '1i'"$NOW - Found Jin's G4"'\' $LOG_FILE
	else
		#echo "Missing ${CURRENTDEV[1]}"
		echo -1 > $DATA_FILE
		echo "$NOW - Missing ${CURRENTDEV[1]}" >> $LOG_FILE
		#sed -i -e '1i'"$NOW - Missing  Jin's G4"'\' $LOG_FILE
	fi
done

# keep first 500 lines in log
#sed -i '501,$ d' $LOG_FILE

# keep last 200 lines in log
LASTDATA=$(tail -n 200 $LOG_FILE)
echo "${LASTDATA}" > $LOG_FILE

exit
