#!/bin/bash
echo Hello
cd /pychronoExp 
git pull
cd /
#/root/miniconda/bin/conda activate 379
python --version
#python -c "print('hello world')"
#python -c "conda activate 379"
python "/pychronoExp/Docker_Repeater/node_env_launch.py"
