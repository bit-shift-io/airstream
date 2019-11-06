Description
============
Developed by Fabian Mathews (supagu@gmail.com). A Webserver that serves temparature probe readings using the Orange Pi Zero (http://www.orangepi.org/orangepizero/)

Install
============

Download Armbian Buster (Debian) and flash to sdcard:

    https://www.armbian.com/orange-pi-zero/

I then resize the partition as for some reason the image leaves most of the sdcard unallocated.

Set up a static IP by editing /etc/network/interfaces
(/etc/dhcpcd.conf for rasberry pi, which has examples at bottom of the file):

    # Ethernet adapter 0
    auto eth0
    allow-hotplug eth0
    #no-auto-down eth0
    iface eth0 inet static
    address 192.168.1.100
    netmask 255.255.255.0
    gateway 192.168.1.3
    dns-nameservers 192.168.1.3
    #dns-nameservers 1.1.1.1 1.0.0.1

Edit /boot/armbianEnv.txt by adding:

    overlays=w1-gpio # was: overlays=usbhost2 usbhost3 w1-gpio
    param_w1_pin=PA10 
    param_w1_pin_int_pullup=1

Edit /etc/default/cpufrequtils changing the last line too:

    GOVERNOR=interactive

OS is now setup, so pop in the sdcard to the orange pi zero, boot it up and we can 
ssh in to root@192.168.1.100. password: 1234
I changed it to qwerty1234
Setup a new account: firefox, zxc


Check the sensors are being detected:

    cat /sys/devices/w1_bus_master1/w1_master_slave_count

This should return the number of sensors hooked up
Now we can test the temparature from on sensor:

    cat /sys/bus/w1/devices/XXXXXXXX/w1_slave

Check out git repo:

    git clone git+ssh://s@192.168.1.2/~/GIT/airstream.git

Run install to install dependencies:

    ./install.sh

To start web server + temp monitor:

    ./main.sh

View webpage at:

    http://192.168.1.100:8000/


Schematic
================
DS1820 Temperature sensor probes use the 1-wire protocol so can just be connected
in parallel.

    https://linux-sunxi.org/Xunlong_Orange_Pi_Zero
    https://kaspars.net/blog/orange-pi-zero-gpio

Pin 4 - 5V - red cable on sensors
Pin 6 - GND - black cable on sensors
Pin 7 - GPIO6 - 4.7Koh resistor to yellow cable 


Dependencies
=================

Chart.js - https://github.com/chartjs/Chart.js
This was cloned
then followed the build instructions:

    npm install
    gulp build

this generates a compiled version of the library with is in the repo

Mako - https://www.makotemplates.org/