#!/bin/bash

sudo sh -c 'echo 0 >/sys/class/leds/led0/brightness'
sudo pigpiod
amixer set PCM,0 100%

cd ~/cuckoo
git pull
# TODO if git pull fails then write to log and commit to repo.

python main.py --fullscreen
# TODO quit the bash script when running main.py
