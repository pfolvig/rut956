
#!/bin/ash
. /rom/usr/share/libubox/jshn.sh
topic=`uci get npe.losant.remote_clientid`
interval=`uci get npe.dio.interval`

while [ true ]; do      
        PAYLOAD=`ubus call ioman.gpio.din1 status`
        json_load "$PAYLOAD"
        json_get_var DIN1 value
        PAYLOAD=`ubus call ioman.gpio.din2 status`
        json_load "$PAYLOAD"
        json_get_var DIN2 value
        PAYLOAD=`ubus call ioman.gpio.dout1 status`
        json_load "$PAYLOAD"
        json_get_var DOUT1 value
        PAYLOAD=`ubus call ioman.gpio.dout2 status`
        json_load "$PAYLOAD"
        json_get_var DOUT2 value
        PAYLOAD=`ubus call ioman.relay.relay0 status`
        json_load "$PAYLOAD"
        json_get_var RELAY1 state
        PAYLOAD=`ubus call ioman.adc.adc0 status`
        json_load "$PAYLOAD"
        json_get_var ANA1 value
        IP=`uci get network.lan.ipaddr`
	json_init
	json_add_object "data"
	json_add_boolean "M_DIN1" $DIN1
	json_add_boolean "M_DIN2" $DIN2
	json_add_boolean "M_OUT1" $DOUT1
	json_add_boolean "M_DOUT2" $DOUT2
        json_add_string "M_RELAY1" $RELAY1
	json_add_double "M_AIN1"  $ANA1
	json_add_string "IP_ADDRESS" $IP
	json_add_string "reg_source" "rutio"
	msg=`json_dump`
	mosquitto_pub -h localhost -m "${msg}"  -t losant/${topic}/state
	sleep ${interval}
done

