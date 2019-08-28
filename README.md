Description
============
Developed by Fabian Mathews (supagu@gmail.com). A Webserver that serves temparature probe readings using the Orange Pi Zero (http://www.orangepi.org/orangepizero/)


Install
============

To install on Armbian Buster (Debian):

    ./install.sh


To start web server + temp monitor:

    ./main.sh


Dependeencies
=================

Chart.js - https://github.com/chartjs/Chart.js
This was cloned
then followed the build instructions:

    npm install
    gulp build

this generates a compiled version of the library

Mako - https://www.makotemplates.org/