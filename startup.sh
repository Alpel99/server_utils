#!/bin/bash
screen -d -m -S minecraft bash -c '$HOME/utils/startmc.sh'
screen -d -m -S factorio_cse bash -c '$HOME/utils/startfactorio_cse.sh'
screen -d -m -S factorio_adrian bash -c '$HOME/utils/startfactorio_adrian.sh'
screen -d -m -S filebrowser bash -c '$HOME/filebrowser/run.sh'
echo "started mc+fc servers"
