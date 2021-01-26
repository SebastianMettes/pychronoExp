import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import json
from gym_multiarm.agent.nodeAgent import agent



##Create a unique ID for host computer
host_id = uuid.uuid4()

##load config.json  
with open("/data/sim/config.json","r") as file:
    config=json.load(file)

#Create agent object
action_agent = agent(config)

#save initialized weights as version 1
action_agent.net.save_model(os.path.join(config("agent_path"),"1"))
agent_version = 1

    
while True:

    #Continuously check for new json files with complete state tensors for each episode

    #Once a sufficient number of files has been obtained, optimze

    #Save the optimized weights in a new directory
    agent_version += 1
    filepath = os.path.join(config("agent_path"),str(agent_version))
    action_agent.net.save_model(filepath)

    #Save the agent optimization config file (in case of crash)

