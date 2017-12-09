#!/usr/bin/env bash
printf "$1" | xxd -pu > data/banner.txt
