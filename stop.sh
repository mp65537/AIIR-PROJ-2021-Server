#!/bin/bash
cd "web-app"
sudo docker-compose down
cd ".."

cd "service"
sudo docker-compose down
cd ".."
