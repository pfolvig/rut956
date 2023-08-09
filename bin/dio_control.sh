#!/bin/ash

. /rom/usr/share/libubox/jshn.sh

while IFS= read -r line; do
  
  json_load "${line}"
  json_select "payload"
  json_get_var "command" command
  json_get_var "port" port
  if [ $command = "set" ] && [ $port = "DOUT2" ]; then
      ubus call ioman.relay.relay0 update '{"state":"closed"}'
      echo "closed"
  else
      if [ $command = "clear" ] && [ $port = "DOUT2" ]; then
          ubus call ioman.relay.relay0 update '{"state":"open"}'
          echo "opened"
      fi
  fi

done
