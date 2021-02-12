#!/bin/bash

sudo docker run --cpus="4" -d -v /data/sim:/data/sim pychrono:latest
sudo docker run --cpus="5" -d -v /data/sim:/data/sim pychrono:latest
sudo docker run --cpus="5" -d -v /data/sim:/data/sim pychrono:latest

