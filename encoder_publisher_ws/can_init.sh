#!/bin/bash
sudo ip link set can0 type can bitrate 500000
sudo ip link set can0 up
sleep 1
cansend can0 000#01
sleep 2
cansend can0 000#01
#sudo chmod 666 /dev/ttyUSB*

#rosrun can_encoder_pub can_encoder_pub_node
