#!/bin/bash

pkill -f playback.py &
python scripts/cleanleds.py &
echo playback.py killed
pkill -f reader.py &
echo reader.py killed