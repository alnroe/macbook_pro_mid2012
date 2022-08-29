#!/bin/bash

if [[ $(id -u) -ne 0 ]]
then
SUDO='sudo'
else
SUDO=''
fi

case "$1" in
us)	
GOVERNOR="userspace"
;;
pr)
GOVERNOR="performance"
;;
ps)
GOVERNOR="powersave"
;;
on)
GOVERNOR="ondemand"
;;
esac

if [[ ! $GOVERNOR ]]
then 
read -p "Select a valid CPU governor (userspace performance powersave ondemand): " GOVERNOR
fi

FREQ=$2

if [[ $GOVERNOR == "userspace" ]]
then
while [ ! $FREQ ] || [ "$FREQ" -lt "800" ] || [ "$FREQ" -gt "1700" ]
do
    read -p "Remember to set a valid frequency! (800-1700 MHz): " FREQ   
done
fi

$SUDO cpupower frequency-set -g $GOVERNOR >/dev/null

echo "CPU Governor set to: ${GOVERNOR}"

if [[ $FREQ ]]
then
$SUDO cpupower frequency-set -f "${FREQ}MHz" >/dev/null

echo "CPU Frequency set to: ${FREQ} MHz"
fi

