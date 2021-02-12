#pychronoExp

Development towards a modular multi-link robotic arm FEA simulation environment following the openAI gym format. IN PROGRESS

Designed to be launched in docker containers which all share the following folder structure:

/data/sim/trial #all simulation results are pushed here under an agent version folder (1,2,3...,n)
/data/sim/agent #updated agents will pushed here under an agent version folder (1,2,...,n)

Can also be run on any PC which contains the above folder structure. 


Files necessary to run program are contained in the Docker folder.

The Master_env_launch.py file launches the environments and optimizer
The node_env_launch.py file launches the simulation environments which continuously run simulations, push results, and check for new agent versions 
/data/sim/config.json contains all training and environment parameters


To run simulations and optimize a network (requires a pytorch supported gpu):

0) Make sure you have the following folder configuration somewhere (easiest directly in c drive):
/data/sim/trial
/data/sim/agent
copy your config.json file into /data/sim/config.json
note: you can obtain a template of config.json under /pychronoexp/Docker

1) build the network container and the fea container:
--navigate to /pychronoexp/Docker
--run: sudo docker build -t pychrono-fea:latest .
--navigate to /pychronoexp/Docker_Host
--run sudo docker build -t pychrono-net:latest .

2) run the network container in order:
--sudo docker run --gpus all -v /data/sim:/data/sim pychrono-net:latest
--sudo docker run -v /data/sim:/data/sim pychrono-fea:latest


Everything should be running
note, these docker images are avaialble via dockerhub under sebastianmettes/pychrono-net and sebastianmettes/pychrono-fea
note, you will create ALOT of data, 100's of gigabytes. You can extract the data using the tools under /pychronoexp/gym-multiarm/gym_multiarm/utilities
