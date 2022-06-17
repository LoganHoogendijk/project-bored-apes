#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

tmux kill-server
cd ~/project-bored-apes
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
tmux new-session -d -s portfolio 'source python3-virtualenv/bin/activate && flask run --host=0.0.0.0'
