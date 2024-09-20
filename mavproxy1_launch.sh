#!/bin/bash
/home/maker/.local/bin/mavproxy.py --master=udpout:192.168.0.101:14552 --out=udp:127.0.0.1:14510 --cmd="set flushlogs True" --state-basedir="/home/maker/drone_telemetry/" --daemon