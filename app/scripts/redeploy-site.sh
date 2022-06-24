#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

cd ~/project-bored-apes
git fetch && git reset origin/main --hard
source python3-virtualenv/bin/activate
pip3 install -r requirements.txt
systemctl daemon-reload
systemctl restart myportfolio
