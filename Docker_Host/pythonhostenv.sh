#!/bin/bash
echo Hello
#/root/miniconda/bin/conda activate 379
python --version
#python -c "print('hello world')"
#python -c "conda activate 379"
cd /pychronoExp
git pull
cd /
python -u "/pychronoExp/Docker/master_env_launch.py"
