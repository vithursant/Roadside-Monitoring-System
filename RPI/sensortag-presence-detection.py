from bluepy.btle import Scanner
from bluepy import sensortag

import os
import sys
import argparse
from time import sleep
import xbee_tx 
from xbee_tx import *

CONTINUOUS = 1

def presence_detection(timeout=20.0, devices=None):
    '''
    Autoscan BLE for neighbouring advertising Sensortag

    @param timeout: The duration for scan timeout (seconds).
    @param devices: The scanned devices using the BLE scanner.

    @return sensor_tags: A dictionary of the sensor tags.
    '''
    sensor_tags = {}
    
    if devices is None:
        ble_devices = Scanner()
        print ("Scanning in Progress \n")
        devices = ble_devices.scan(timeout)

    dev_list='List : \n'
    for dev in devices:
        if 'SensorTag' in str(dev.getValueText(9)):
            print ("Device %s (SensorTag), RSSI=%d dB" % (dev.addr, dev.rssi))
            dev_list = dev_list + "Device %s (SensorTag), RSSI=%d dB \n" % (dev.addr, dev.rssi)
            sensor_tags[dev.addr] = dev.rssi

    if sensor_tags is None:
        print ("No SensorTags found in the zone")
        
    return sensor_tags
     
        
def start_construction_worker_detection():
    if not os.geteuid() == 0:
        sys.exit('Script must be run as root')

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', action='store', default=20.0, type=float, help="SensorTag scan timeout duration (seconds).")
    parser.add_argument('-s',action='store', default=10.0, type=float, help='Sleep time (seconds) between scanning for devices.')
    arg = parser.parse_args(sys.argv[1:])

    timeout = arg.t
    sleep_time = arg.s
    
    print ("Detecting Presence of Construction Workers")

    # Continuous monitoring
    while CONTINUOUS:
        sensor_tags = presence_detection(timeout)
        print (sensor_tags)
        sleep(sleep_time)
        if len(sensor_tags) > 0:
            print('Sending to Laptop')
            xbee_write(60)	
    print ("Done Scanning")
 
if __name__ == '__main__':
    start_construction_worker_detection()
 

