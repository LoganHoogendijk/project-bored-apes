#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

curl -X POST http://localhost:5000/api/timeline_post -d 'name=Test&email=test@gmail.com&content=Testing endpoints with a script!'
curl http://localhost:5000/api/timeline_post
#curl -X DELETE http://localhost:5000/api/timeline_post
