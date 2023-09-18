#!/bin/bash
source /home/camilo/utils/utils.config

# check for someone online
reswho=$(/usr/bin/who | wc -l)
if [ "$reswho" -ne "0" ]; then
	echo "someone is working on the server, exit"
	exit
fi	

# check for running screen sessions
resscreen=$(screen -ls | wc -l)
if [ "$resscreen" -eq "2" ] && $activated_shutdown; then
       	echo "no screen session running, shutdown"
	/bin/bash /home/camilo/utils/shutdown.sh
	exit
fi

log="/home/camilo/minecraft/logs/latest.log"
/usr/bin/screen -S minecraft -X stuff "/list^M"

sleep 0.1
resmc=$(tail -n 1 "$log" | sed -E 's/.*are ([0-9]+) of.*/\1/')

# echo $res
# check for mc players
if [ "$resmc" -gt "0" ]; then
	echo "mc server not empty"
	exit
fi

resfc1=$(jq '.players | length' /home/camilo/factorio_cse/factorio/player-data.json)
# echo $resfc
# check for factorio players
if [ "$resfc1" -gt "0" ]; then
	echo "factorio server (cse) not empty"
	exit
fi

resfc2=$(jq '.players | length' /home/camilo/factorio_adrian/factorio/player-data.json)
# echo $resfc
# check for factorio players
if [ "$resfc2" -gt "0" ]; then
	echo "factorio server (adrian) not empty"
        exit
fi

# check for activated shutdown switch in ./utils.config
if [ "$activated_shutdown" == "false" ]; then
	echo "shutdown is deactivated"
	exit
fi

#shutdown after delay time
if [ "$resfc1" -eq "0" ] && [ "$resfc2" -eq "0" ] && [ "$resmc" -eq "0" ] && $activated_shutdown; then
	echo "noone online, will check for shutdown in $utils_delay sec"
	sleep $utils_delay
	# check all the necessary stuff again
	source /home/camilo/utils/utils.config
	reswho=$(/usr/bin/who | wc -l)
	if [ "$reswho" -ne "0" ]; then
	        echo "someone is working on the server, exit"
	        exit
	fi
	/usr/bin/screen -S minecraft -X stuff "/list^M"
	sleep 0.1
	resmc=$(tail -n 1 "$log" | sed -E 's/.*are ([0-9]+) of.*/\1/')
	resfc1=$(jq '.players | length' /home/camilo/factorio_cse/factorio/player-data.json)
	resfc2=$(jq '.players | length' /home/camilo/factorio_adrian/factorio/player-data.json)
	if [ "$resfc1" -eq "0" ] && [ "$resfc2" -eq "0" ] && [ "$resmc" -eq "0" ] && $activated_shutdown; then
		/bin/bash /home/camilo/utils/shutdown.sh
	fi
fi
