#!/bin/bash

python playback.py &
echo playback.py started
python reader.py &
echo reader.py started