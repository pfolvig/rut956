#!/bin/ash
topic=`uci get npe.losant.remote_clientid`

dhcp=`uci show dhcp | grep comap | cut -f1 -d\=| sed s/name/ip/`
host=`uci get ${dhcp}`
enabled=`uci get npe.comap.enabled`
export PYTHONPATH=/root/lib:/root/registers
if [ "$enabled" = "1" ] 
  then {
	echo "Starting losant monitoring -c ${host} ${topic}"
	logger -t "Losant" "Monitoring ${host} publishing to ${topic}"
	/root/bin/modbus.py comap_registers -n ${host} -t "losant/${topic}/state" -i 4 --offset 1
	} fi
