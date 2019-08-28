#!/usr/bin/env python3
# -*- coding: utf_8 -*-

#
# 2018 - Fabian Mathews - supagu@gmail.com
#
# http://www.modmypi.com/blog/ds18b20-one-wire-digital-temperature-sensor-and-the-raspberry-pi
#
# * Running with no arguments will run in an infinite loop dumping temps to console
#
# * Running with an argument supplied, the probe name such as:
#         python temp.py 3ff
# will output the temp of 3ff to console for use with Cacti (http://www.cacti.net/)
#
#


import os
import time
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

tempSensorPathArray = {
  "eff": "/sys/bus/w1/devices/28-031504994eff/w1_slave",
  "3ff": "/sys/bus/w1/devices/28-0115154e93ff/w1_slave",
  "dff": "/sys/bus/w1/devices/28-031504c68dff/w1_slave"
}

history = {
  "eff": [0, 2, 3],
  "3ff": [2, 2, 2],
  "dff": [0, 0, 0]
}

history_length = 10

sleep_time_sec = 30
  
def temp_raw(tempSensorName):
    f = open(tempSensorPathArray[tempSensorName], 'r')
    lines = f.readlines()
    f.close()
    return lines
    
def read_temp(tempSensorName):
    lines = temp_raw(tempSensorName)
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = temp_raw(tempSensorName)
        
    temp_output = lines[1].find('t=')

    if temp_output != -1:
        temp_string = lines[1].strip()[temp_output+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


def poll_temps_foreever():
  while True:
    for tempSensor in tempSensorPathArray:
      try:
        history[tempSensor].append(read_temp(tempSensor))
        del history[tempSensor][history_length:] # clip history to a certain length
      except:
        print("Err with sensor: " + tempSensor)

    time.sleep(sleep_time_sec)
         


if __name__ == '__main__':        
  if len(sys.argv) == 2:
    print(str(read_temp(sys.argv[1])))
    sys.exit()
    
  # go into an infinite loop for testing
  print("Starting temp probe infinite loop")
  while True:
      print("EFF: " + str(read_temp("eff")))
      print("3FF: " + str(read_temp("3ff")))
      print("DFF: " + str(read_temp("dff")))
      print("")
      time.sleep(1)
        
        