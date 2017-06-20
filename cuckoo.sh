#!/bin/bash
cd ~/cuckoo
git pull
# TODO if git pull fails then write to log and commit to repo.
python main.py --fullscreen
# TODO quit the bash script when running main.py
