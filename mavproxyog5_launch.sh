#!/bin/bash
/home/maker/.local/bin/mavproxy.py --master=udpout:192.168.0.112:14552 --out=udp:127.0.0.1:14590 --cmd="set flushlogs True" --state-basedir="/home/maker/drone_telemetry/" --daemon