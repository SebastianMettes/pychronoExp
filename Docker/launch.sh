#!/bin/bash

sudo docker run --cpus="4" -d -v /data/sim:/data/sim -v /data/cold:/data/cold sebastianmettes/pychrono-fea-radius:latest
sudo docker run --cpus="4" -d -v /data/sim:/data/sim -v /data/cold:/data/cold sebastianmettes/pychrono-fea-radius:latest

sudo docker run --cpus="4" -d -v /data/sim:/data/sim -v /data/cold:/data/cold sebastianmettes/pychrono-fea-radius:latest

sudo docker run --cpus="4" -d -v /data/sim:/data/sim -v /data/cold:/data/cold sebastianmettes/pychrono-fea-radius:latest


