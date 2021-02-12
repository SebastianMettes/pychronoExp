#!/bin/bash

sudo docker run --gpus all --cpus="2" -d -v /data/sim:/data/sim pychronohost:latest

