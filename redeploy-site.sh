#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

cd ~/project-bored-apes
git fetch && git reset origin/main --hard
docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
