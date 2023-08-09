#!/bin/ash
topic=`uci get npe.losant.remote_clientid`

logger -t "Losant" "Subcribing to ${topic}"
mosquitto_sub -t losant/${topic}/command -h localhost | /root/bin/dio_control.sh
