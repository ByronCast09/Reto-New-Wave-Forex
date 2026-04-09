#!/bin/bash
echo "Building Project..."
python3 -m pip install -r requirements.txt
python3 waveForex/manage.py collectstatic --noinput --clear
echo "Build complete."
