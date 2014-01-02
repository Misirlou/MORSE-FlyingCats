#!/bin/bash
echo "Starting simulation Environment"
morse run scene.py 1>/dev/null 2>&1 &
sleep 60s
echo "Starting Agents"
python3  runner.py 1>/dev/null 2>&1 &
python3  chaser.py 1>/dev/null 2>&1 &
ipython3 referee.py --pylab