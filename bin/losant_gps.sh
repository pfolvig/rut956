#!/bin/ash
. /rom/usr/share/libubox/jshn.sh
topic=`uci get npe.losant.remote_clientid`

while [ true ]; do
	GPS=`gpsctl -i -x -a -v -u -g -p `
	set -- ${GPS}
	echo $1
	json_init
	json_add_object "data"
	json_add_string "M_GPS" "$1,$2"
	json_add_double "M_ALTITUDE" $3
	json_add_double "M_VELOCITY" $4
	json_add_double "M_ACCURACY" $5
	json_add_double "M_ANGLE" $6
	json_add_double "M_SATCOUNT" $7
	json_add_string "reg_source" "gps"

	msg=`json_dump`
	echo $msg
	mosquitto_pub -h localhost -m "${msg}"  -t losant/${topic}/state
	sleep 300
done
