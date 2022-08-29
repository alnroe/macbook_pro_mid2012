#!/bin/python3

import subprocess
import time

MANUAL = '/sys/devices/platform/applesmc.768/fan1_manual'
RPM = '/sys/devices/platform/applesmc.768/fan1_output'
LOG = '/home/me/temp.log'

def temps():

    """ Restituisce le temperature di sensors nel seguente ordine:
        Package Id 0
        Core 0
        Core 1
    """

    # E se usassi grep?

    f = subprocess.run('sensors', capture_output=True)

    string = f.stdout.decode('utf-8')

    arr = string.split('\n')

    raw_temps = []

    for i,n in enumerate(arr):
        if i in [37, 38, 39]:
            raw_temps.append(n)

    temps = []

    for item in raw_temps:
        sub = item.split(':')
        sub1 =sub[1].split('°')
        temps.append(float(sub1[0].strip()[1:]))

    return temps

def fan_control(temps):

    """Profili di risposta velocità ventole - temperatura, non sarebbe male introdurne più di uno
        > 67 => 6200
        61 - 67 => 5500
        58 - 61 => 5000
        54-58 => 4500
        <54 => 3200

    Inserire check su fan1_manual, all'avvio - controllare temperature, non mi sembra ben calibrato
    """

    def write_rpm(rpm, temp):

        with open(MANUAL, 'r+') as control:
            if control.read(1) == '0':
                control.write('1')
            else:
                pass

        with open(RPM, 'w') as output:
            output.write(str(rpm))
        with open(LOG, 'a') as log:
            log.write(f'{time.ctime()}, {temp}°C = > {rpm} RPM\n')

    t = temps[1]

    if t <= 53:
        write_rpm(3400, t)
    elif t > 53 and t <= 58:
        write_rpm(4000, t)
    elif t > 58 and t <= 61:
        write_rpm(4500, t)
    elif t > 61 and t <= 64:
        write_rpm(5000, t)
    else:
        write_rpm(6200, t)


t = temps()
print(t)

fan_control(t)