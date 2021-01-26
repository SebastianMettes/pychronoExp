#pychronoExp

Development towards a modular multi-link robotic arm FEA simulation environment following the openAI gym format. IN PROGRESS

Currently environment is not functional

Designed to be launched in docker containers which all share the following folder structure:

/data/sim/trial #all simulation results are pushed here under an agent version folder (1,2,3...,n)
/data/sim/agent #updated agents will pushed here under an agent version folder (1,2,...,n)

Can also be run on any PC which contains the above folder structure. 


Files necessary to run program are contained in the Docker folder.

The Master_env_launch.py file launches the environments and optimizer
The node_env_launch.py file launches the simulation environments which continuously run simulations, push results, and check for new agent versions 
config.json contains all training and environment parameters


Useful information:

-PyChrono module: conda install -c projectchrono pychrono

-run in a python 3.7.x virtual environment
