# Server utils

Main goal is to lower power consumption of a home server, by shutting it down, while noone is using it.

# other important commands/info

## systemd unit
in /etc/systemd/system
### utils.service
```
[Unit]
Description=Utils to shutdown server if noone is online

[Service]
Type=forking
User=camilo
Group=camilo
TimeoutSec=310
ExecStart=/usr/bin/python3 home/camilo/utils/shutdown_query.py
```

### utils.timer
```
[Unit]
Description=Utility to shutdown server if noone is online

[Timer]
OnBootSec=10min
OnUnitActiveSec=5min
Unit=utils.service

[Install]
WantedBy=timers.target
```

## server startups

### mc - run.sh
```bash
#!/bin/bash
NUM="${1:-1536}"
java -Xmx"$NUM"M -Xms"$NUM"M -jar server.jar nogui
```

### factorio - run.sh
```bash
#!/bin/bash
./factorio/bin/x64/factorio --start-server save1.zip --server-settings server-settings.json --port 34198 | tee factorio-console.log
```

## execute commands in screen sessions:
Using screen -X stuff and a newline char at the end of command to execute.
```bash
/usr/bin/screen -S minecraft -X stuff "/list^M"
```

## server status

* hosts a webserver for json request of server status
* used for [eink display](https://github.com/Alpel99/eink_status)
