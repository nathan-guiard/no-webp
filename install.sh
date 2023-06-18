#!/bin/bash

apt install python3.10-venv -y
status=$?
if [ ! $status -eq 0 ]; then
	exit $status
fi

# initializing no-webp directory
mkdir -p /opt/no-webp/
cp -r src /opt/no-webp/
cp example_config/default.yml /opt/no-webp/config.yml
cp start.sh /opt/no-webp/


#creating your config file
echo -e '\033[1m---CONFIGURATION SETUP---\033[0m'
EXT=".jpg"
echo "What extention do you want to convert your .webp files to? (default $EXT)"
read EXT
if [ -z $EXT ]; then
	EXT=".jpg"
fi

DIR="/home/$SUDO_USER/Downloads"
echo "Which directory do you want to monitor? (default $DIR)"
read DIR
if [ -z $DIR ]; then
	DIR="/home/$SUDO_USER/Downloads"
fi
if [ ! -d $DIR ]; then
	echo -e "\033[33mWARNING:\033[0m $DIR is not a directory. This setting can be changed in /opt/no-webp/config.yml\n"
fi

PKG='/usr/bin/convert'
echo "Which package do you want to use to convert? (default $PKG)"
echo -e '\033[35mNOTE:\033[0m the package should be used like this:\npackage <file to convert> <output file>'
read PKG
if [ -z $PKG ]; then
	PKG='/usr/bin/convert'
fi
which $PKG 1>/dev/null 2>&1 || echo "\033[33mWARNING:\033[0m $PKG not found. This setting can be changed in /opt/no-webp/config.yml"

sed -i "s#EXT#$EXT#" /opt/no-webp/config.yml
sed -i "s#DIR#$DIR#" /opt/no-webp/config.yml
sed -i "s#PKG#$PKG#" /opt/no-webp/config.yml

echo 'Configuration complete!'
echo -e 'You can change this configuration in /opt/no-webp/config.yml\n'

SYS=$(ps -p 1 -o comm=)

if [ $SYS = 'systemd' ]; then
	cp no-webp.service /etc/systemd/system/
else
	echo -e "033[31;1mERROR:\033[0m Your os is not started by a systemd. I dont know how to create a daemon. Check your system's documentation."
	exit 1
fi

# virtual env
cd /opt/no-webp
python3 -m venv no-webp_env


echo -e "\033[32mInstallation complete\033[0m"

echo "Starting the daemon"
systemctl start no-webp

echo 'Waiting for daemon to start (3sec)'
sleep 3
if systemctl is-active --quiet no-webp; then
	echo 'Everything went well, daemon started.'
else
	echo 'The daemon did not start, try to check the logs.'
fi

