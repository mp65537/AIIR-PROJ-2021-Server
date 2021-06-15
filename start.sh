#!/bin/bash
NODES_NUM=4
cd "service"
sudo docker-compose up --build -d --scale head-node=1 --scale worker-node=${NODES_NUM}
sudo docker-compose exec -d --privileged head-node mpirun --allow-run-as-root -n ${NODES_NUM} python3 /home/mpirun/builder/main.py
cd ".."

cd "web-app"
sudo docker-compose up --build -d
cd ".."

