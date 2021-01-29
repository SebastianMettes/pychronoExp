#!/bin/bash

sudo docker run --gpus all --cpus="2" -v /data/sim:/data/sim pychronohost:latest

