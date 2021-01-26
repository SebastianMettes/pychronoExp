import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import os.path
import json
from gym_multiarm.agent.nodeAgent import agent
import time
import numpy as np

##Create a unique ID for host computer
host_id = uuid.uuid4()

##load config.json  
with open("/data/sim/config.json","r") as file:
    config=json.load(file)

#Create agent object and related components
action_agent = agent(config)
objective = nn.CrossEntropyLoss
optimizer = optim.Adam(params = action_agent.net.parameters(),lr = config['learning_rate'])
sm = nn.Softmax(dim=1)

#save initialized weights as version 1
agent_version = 1
filepath = os.path.join(config["agent_path"],str(agent_version))
action_agent.net.save_model(filepath)

#modules:
def update_agent_filepath(config,agent_version):
    filepath = os.path.join(config["agent_path"],str(agent_version))
    return(filepath)

def optimal_state_tensor(config,file_list,agent_version):
    episodes = []
    for i in range(0,len(file_list)):
        with open(os.path.join(config['agent_path'],str(agent_version),file_list[i])) as file:
            state_tensor = json.load(file)
            states, _, actions, rewards = zip(*state_tensor)
            state_tensor = zip(
                torch.FloatTensor(states),
                torch.nn.functional.one_hot(torch.LongTensor(actions),config['N_ACTIONS']),
                torch.FloatTensor(rewards)
                )
            episodes.append((sum(rewards),state_tensor))

    #Episodes is a list of the following form
    #[ (Er0,[(s0,a0,r0),(s1,a1,r1),...]), (Er1, [(s0,a0,r0)...])]

    #Filter episodes
    rewards, _ = zip(*episodes)
    reward_cutoff = np.percentile(rewards,config["PERCENTILE"],overwrite_input=True)

    episodes = list(filter(lambda x: x[0] >= reward_cutoff,episodes))
    _, filtered_state_tensors = zip(*episodes)

    return filtered_state_tensors


    



    
while True:
    while True:
    #Continuously check for new json files with complete state tensors for each episode
        #create an array of filenames
        file_list = [name for name in os.listdir(filepath) if os.path.isfile(os.path.join(filepath,name))]
        time.sleep(5)
        if len(file_list) >= config['BATCH_SIZE']:
            break
        
    #import files into usable arrays.
        optimal_tensor = optimal_state_tensor(config,file_list,agent_version)
    
    #optimize:
        obs_v, act_v, _ = zip(*optimal_tensor)
        obs_v = torch.stack(obs_v)
        act_v = torch.stack(act_v)

        optimizer.zero_grad()
        action_scores_v = action_agent(obs_v)
        loss_v = objective(action_scores_v,acts_v)
        loss_v.backward()
        optimizer.step()
        print('successfully optimized %d',agent_version+1)



 
        


    #Save the optimized weights in a new directory
    agent_version = agent_version+=1
    filepath = update_agent_filepath(config,agent_version)
    action_agent.net.save_model(filepath)

    #Save the agent optimization config file (in case of crash)
