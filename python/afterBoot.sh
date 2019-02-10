#!/bin/bash
# one-liner to find current location
PBAPI="YtymmlWfUVlATvPbHP1UW8u1MrDqlNdU"
PBDEV="udqhCsjAnpRXKnLg"

sleep 20
curl -u $PBAPI: https://api.pushbullet.com/v2/pushes -d device_iden="$PBDEV" -d type=note -d title="Alastair" -d body="rPi has just booted up." > /dev/null