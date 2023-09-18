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
ExecStart=/home/camilo/utils/query.sh
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
```
#!/bin/bash
NUM="${1:-1536}"
java -Xmx"$NUM"M -Xms"$NUM"M -jar server.jar nogui
```

### factorio - run.sh
```
#!/bin/bash
./factorio/bin/x64/factorio --start-server save1.zip --server-settings server-settings.json --port 34198
```
