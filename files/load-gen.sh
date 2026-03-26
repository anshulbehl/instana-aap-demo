#!/bin/bash
# Background load generator - sends requests to the demo app
while true; do
  curl -s -o /dev/null http://localhost:8080/api/checkout
  sleep 0.5
done
