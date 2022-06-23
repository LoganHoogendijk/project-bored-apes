#!/bin/bash
# Author: Logan Hoogendijk
# Script follows below:

echo "Printing requests to see which to delete"
curl http://localhost:5000/api/timeline_post

read -p "Enter ID for post to delete: " id
curl -X DELETE http://localhost:5000/api/timeline_post/$id

echo "Printing requests to check it deleted"
curl http://localhost:5000/api/timeline_post
