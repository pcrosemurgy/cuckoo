#!/bin/bash
sudo pigpiod
amixer set PCM,0 90%
sudo hub-ctrl -h 0 -P 2 -p 0
sudo sh -c 'echo 0 >/sys/class/leds/led0/brightness'

cd ~/cuckoo
git pull
python main.py --fullscreen
