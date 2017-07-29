#!/bin/bash

sudo sh -c 'echo 0 >/sys/class/leds/led0/brightness'
sudo pigpiod
amixer set PCM,0 100%
# TODO disable auto screen turn off

cd ~/cuckoo
git pull

5_DAYS_AGO = "$(date -d 'now - 5 days' +%s)"
GIF_TIME = "$(ls data/img/week/*.gif -d | tail -1)"
if (( GIF_TIME <= 5_DAYS_AGO )); then
    python gif_downloader.py & # TODO only call this every week. Check date on data/img/week .gif
fi

python main.py --fullscreen
