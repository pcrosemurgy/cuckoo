#!/bin/bash

sudo pigpiod
amixer set PCM,0 100%
sudo hub-ctrl -h 0 -P 2 -p 0
sudo sh -c 'echo 0 >/sys/class/leds/led0/brightness'

cd ~/cuckoo
git pull

5_DAYS_AGO = "$(date -d 'now - 5 days' +%s)"
GIF_TIME = "$(ls data/img/week/*.gif -d | tail -1)"
if (( GIF_TIME <= 5_DAYS_AGO )); then
    python gif_downloader.py &
fi

python main.py --fullscreen
