#!/bin/ash
opkg update
opkg install mosquitto-ssl mosquitto-client-ssl
opkg install python3 python3-pip
opkg install coreutils-nohup
opkg install python3-light
opkg install python3-codecs
opkg install python3-decimal
opkg install python3-logging
opkg install python3-pyserial

timeout=30

chmod -R a+x /root/*

uci import < /root/uci/npe.uci

cp /root/config/mosquitto_template.conf /root/config/mosquitto.conf

CLIENTID=`uci get npe.losant.remote_clientid`
USERNAME=`uci get npe.losant.remote_username`
PASSWORD=`uci get npe.losant.remote_password`

sed -i "s/<deviceid>/$CLIENTID/g" /root/config/mosquitto.conf
sed -i "s/<accesskey>/$USERNAME/g" /root/config/mosquitto.conf
sed -i "s/<accesspassword>/$PASSWORD/g" /root/config/mosquitto.conf

cp /root/init.d/* /etc/init.d
cp /root/config/mosquitto.conf /etc/mosquitto/mosquitto.conf

/etc/init.d/losant_rutio enable
/etc/init.d/losant_command enable
/etc/init.d/losant_gps enable
/etc/init.d/losant_solar enable
/etc/init.d/losant_comap enable

echo -e "\n"
echo "Make sure to set the static lease for "comap" at ***.***.***.051"
echo -e "\n"

echo "Do you want to reboot now? (y/n): "
# Wait for 30 seconds. If no input is received, proceed as if 'n' was entered
read -t 30 choice

# If read times out, $? is 1, so we can handle that scenario
if [ $? -eq 1 ]; then
    echo "Timed out waiting for input. Not rebooting."
    exit 1
fi

# Check the user's choice and reboot if 'y' or 'Y'
case $choice in
    [yY]* )
        echo "Rebooting now..."
        sudo reboot
        ;;
    [nN]* )
        echo "Not rebooting."
        ;;
    * ) 
        echo "Invalid choice."
        ;;
esac
