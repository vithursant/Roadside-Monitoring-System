#!/usr/bin/python

#https://www.raspberrypi.org/forums/viewtopic.php?p=597417#p597417
#https://www.raspberrypi.org/forums/viewtopic.php?p=600981#p600981

# comment out the lines specified in the bove posts
# on raspberry pi 3 you need to set "enable_uart=1"
# in /boot/config.txt

import serial
import time
ser = serial.Serial("/dev/ttyS0",baudrate=9600)
idx = 0

#while True:
#  	print idx
#  	ser.write(str(idx))
#  	ser.write("\r\n") 
#  	time.sleep(1)
#  	idx = idx + 1

def xbee_write(data):
  	ser.write(str(data))
  	ser.write("\r\n")
