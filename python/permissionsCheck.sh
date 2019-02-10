#!/bin/bash
# one-liner to find current location
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

cd "$DIR"
chown pi:pi *
chmod -R 755 *.sh

cd "$DIR/logs"
chown pi:www-data *
chmod -R 666 *

#old codes
#chmod 775 "$DIR/logs/"
#chown -R pi:www-data "$DIR/logs"
#chmod -R 666 "$DIR/logs/."