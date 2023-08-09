#!/bin/ash

topic=`uci get npe.losant.remote_clientid`
port=`uci get npe.solar.port`
interval=`uci get npe.solar.interval`
enabled=`uci get npe.solar.enabled`

export PYTHONPATH=/root/lib:/root/registers

if [ "$enabled" = "1" ]
    then {
		echo "Losant enabled"
		echo "Starting losant solar monitoring -c ${port} losant/${topic}/state ${interval}"
		logger -t "losant" "Starting losant solar monitoring -c ${port} losant/${topic}/state ${interval}"
		/root/bin/modbus.py  solar_registers -t "losant/${topic}/state" -p ${port} -i ${interval} 
       
    }  fi