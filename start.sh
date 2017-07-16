#!/bin/bash

sudo sh -c 'echo 0 >/sys/class/leds/led0/brightness'
sudo pigpiod
amixer set PCM,0 100%
# TODO disable auto screen turn off

cd ~/cuckoo
git pull
# TODO if git pull fails then write to log and commit to repo.

python gif_downloader.py & # TODO only call this every week. Check date on data/img/week .gif
python main.py --fullscreen
