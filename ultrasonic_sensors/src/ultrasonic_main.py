#!/usr/bin/env python
#### Created by SUTD ROAR LAB ####

import rospy
from std_msgs.msg import Int32MultiArray
from geometry_msgs.msg import Twist
import serial
import struct
import time
import sys
import linbus_ultrasonic as ultra
from bitarray import bitarray # pip install bitarray
import bitarray.util as util
from binascii import hexlify
import serial.tools.list_ports

class RosHandler:

    def __init__(self):
        self.sn1 = 'A505HSMR'
        p = list(serial.tools.list_ports.grep(self.sn1))
        self.port = '/dev/' + p[0].name
        self.data_publisher = rospy.Publisher("/ultrasonic_data", Twist, queue_size=3)
        print("Running")
        self.ultrasonic_sensor1 = ultra.Ultrasonic(self.port) # Check serial port address
        #self.ultrasonic_sensor2 = ultra.Ultrasonic('/dev/ttyUSB3',debug=True, address=1)
        self.distance1 = 0
        self.distance2 = 0
        self.address1 = 0

    def run(self):

        while not rospy.is_shutdown():
            #self.distance = self.ultrasonic_sensor._checksum([167,54,85])
            self.distance1 = self.ultrasonic_sensor1.measure()
            #self.distance2 = self.ultrasonic_sensor2.measure()
            #print(self.distance) # 115
            print("distance1 :", self.distance1)
            print("distance2: ", self.distance2)
            data_array = Twist()

            data_array.linear.x = self.distance1
            data_array.linear.y = self.distance2
            data_array.linear.z = 0
            data_array.angular.x = 0
            data_array.angular.y = 0
            data_array.angular.z = 0

            self.data_publisher.publish(data_array)
            
            rate.sleep()
        return 

    def set_address(self):
        new_addr = input("Enter new address: ")
        self.ultrasonic_sensor1.setAddress(new_addr)
        self.address1 = new_addr

    def offPWM(self):
        self.ultrasonic_sensor1.off_PWM()

if __name__ == '__main__':
    rospy.init_node('ultrasonic_sensor')
    rate = rospy.Rate(10) # 10hz
    rh = RosHandler()
    #rh.run()
    while not rospy.is_shutdown():
        usr_inp = input("Enter mode:\n 1. Set Address\n 2. Measure\n")
        if usr_inp == 1:
            rh.set_address()
        elif usr_inp == 2:
            rh.run()
        elif usr_inp == 3:
            rh.offPWM()