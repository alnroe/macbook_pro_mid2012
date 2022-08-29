#/bin/bash

# Fan control macbook pro 2012
CHECK="/sys/devices/platform/appelsmc.768/fan1_manual"
FILE="/sys/devices/platform/applesmc.768/fan1_output"

if [[ $(id -u) -ne 0 ]]
then
SUDO='sudo'
else
SUDO=''
fi

if [[ $(cat $CHECK) -ne 1 ]]
then
$SUDO bash -c "echo 1 > $CHECK"
fi

RPM=$1

if [[ $RPM ]]
then
$SUDO bash -c "echo $RPM > $FILE"
else
read -p "Select RPM: " RPM
	if [[ "$RPM" -gt "2000" && "RPM" -lt "6200" ]]
	then
	$SUDO bash -c "echo $RPM > $FILE"
	fi
fi

