#!/bin/bash

echo "Pause for $1 seconds"

sleep $1

DISPLAY=:0 python3 /home/pi/Rocket-dashboard/main_program_v4.py

echo "Done"
