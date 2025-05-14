#!/bin/ash
opkg update --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install mosquitto-ssl mosquitto-client-ssl --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3 python3-pip --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install coreutils-nohup --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3-light --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3-codecs --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3-decimal --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3-logging --force_feeds /etc/opkg/openwrt/distfeeds.conf
opkg install python3-pyserial --force_feeds /etc/opkg/openwrt/distfeeds.conf

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

mkdir -p /etc/mosquitto/certs
cp /root/certs/Losant_CA.crt /etc/mosquitto/certs/
chmod 644 /etc/mosquitto/certs/Losant_CA.crt

echo "Enabling GPS"
uci set gps.gpsd.enabled='1'    
uci set gps.gpsd.galileo_sup='1'    
uci set gps.gpsd.glonass_sup='7'    
uci set gps.gpsd.beidou_sup='3'

/etc/init.d/losant_rutio enable
/etc/init.d/losant_command enable
/etc/init.d/losant_gps enable
/etc/init.d/losant_solar enable
/etc/init.d/losant_comap enable
/etc/init.d/losant_gps enable

# add firewall rule
uci set firewall.25=rule
uci set firewall.25.src='wan'
uci set firewall.25.name='Allow VPN Webaccess'
uci set firewall.25.target='ACCEPT'
uci set firewall.25.priority='15'
uci add_list firewall.25.dest_port='80'
uci add_list firewall.25.dest_port='443'
uci set firewall.25.proto='tcp'
uci set firewall.25.enabled='1'
uci add_list firewall.25.src_ip='192.168.0.0/16'
uci add_list firewall.25.src_ip='192.168.28.0/24'
uci add_list firewall.25.src_ip='192.168.4.0/23'
uci set firewall.25.extra='-m policy --dir in --pol ipsec --mode tunnel --tunnel-dst 0.0.0.0/0 --tunnel-src 0.0.0.0/0'
# enable ssh wan
uci set firewall.15.enabled='1'
uci commit

# reload the firewall daemon
/etc/init.d/firewall reload

echo -e "\n"
echo "Make sure to set the static lease for "comap" at ***.***.***.051"
echo -e "\n"

echo "Do you want to reboot now? (y/n): "
# Wait for 300 seconds. If no input is received, proceed as if 'n' was entered
read -t 300 choice

# If read times out, $? is 1, so we can handle that scenario
if [ $? -eq 1 ]; then
    echo "Timed out waiting for input. Not rebooting."
    exit 1
fi

# Check the user's choice and reboot if 'y' or 'Y'
case $choice in
    [yY]* )
        echo "Rebooting now..."
        reboot
        ;;
    [nN]* )
        echo "Not rebooting."
        ;;
    * ) 
        echo "Invalid choice."
        ;;
esac
