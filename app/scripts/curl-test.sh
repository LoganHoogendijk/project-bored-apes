#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

curl -X POST http://localhost:5000/api/timeline_post -d 'name=Test&email=test@gmail.com&content=Testing endpoints with a script!'

echo "Printing requests"
curl http://localhost:5000/api/timeline_post

echo "Enter ID for post to be deleted: "
read $id
curl -X DELETE http://localhost:5000/api/timeline_post/$id

echo "Printing requests again"
curl http://localhost:5000/api/timeline_post
