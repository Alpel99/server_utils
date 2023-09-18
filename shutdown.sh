#!/bin/bash
echo "server will be shutdown"
screen -S minecraft -X stuff '/stop^M'
screen -S factorio_cse -X stuff '/quit^M'
screen -S factorio_adrian -X stuff '/quit^M'
screen -S filebrowser -X stuff '^C'

sleep 10

sudo /sbin/shutdown now

