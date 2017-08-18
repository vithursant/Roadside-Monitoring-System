#! /bin/sh

python worker_detect.py &
worker_detect_PID=$!
sudo python sensortag-presence-detection.py &
sensortag_PID=$!