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


##load config.json  
with open("/data/sim/config.json","r") as file:
    config=json.load(file)

#Create agent object and related components
action_agent = agent(config)
objective = nn.CrossEntropyLoss()
optimizer = optim.Adam(params = action_agent.net.parameters(),lr = config['learning_rate'])
sm = nn.Softmax(dim=1)

#OUTPUT DATA ARRAY
##Check if previous version exists:
data = []
#if os.path.isfile(os.path.join(config["agent_path"],'data.csv')) == True:
    #data = np.loadtxt(os.path.join(config["agent_path"],'data.csv'),  delimiter=",")

#modules:
def update_agent_filepath(config,agent_version):
    filepath = os.path.join(config["agent_path"],str(agent_version))
    
    trialpath = os.path.join(config["save_dir"],str(agent_version))
    if os.path.isdir(trialpath) == False:
        os.mkdir(trialpath)
        os.system(f"chmod 777 {trialpath}")
    return(filepath,trialpath)

def optimal_state_tensor(config,file_list,agent_version):
    episodes = []

    for i in range(0,len(file_list)):
        #print(os.path.join(config['save_dir'],str(agent_version),file_list[i]))
        with open(os.path.join(config['save_dir'],str(agent_version),file_list[i])) as file:
            state_tensor = json.load(file)
            states, _, actions, rewards = zip(*state_tensor)
            state_tensor = (
                torch.FloatTensor(states),
                #torch.nn.functional.one_hot(torch.LongTensor(actions),config['N_ACTIONS']),
                torch.LongTensor(actions),
                torch.FloatTensor(rewards)
                )

            episodes.append((sum(rewards),state_tensor))

    #Episodes is a list of the following form
    #[ (Er0,[(s0,a0,r0),(s1,a1,r1),...]), (Er1, [(s0,a0,r0)...])]

    #Filter episodes

    rewards, _ = zip(*episodes)
    
    reward_cutoff = np.percentile(rewards,config["PERCENTILE"],overwrite_input=True)
    episodes = list(filter(lambda x: x[0] >= reward_cutoff,episodes))
    rewards, filtered_state_tensors = zip(*episodes)
    

    return np.mean(rewards), filtered_state_tensors


    
#save initialized weights as version 1
agent_version = 1
filepath,trialpath = update_agent_filepath(config,agent_version)

action_agent.net.save_model(filepath)


    
while True:
    while True:
    #Continuously check for new json files with complete state tensors for each episode
        #create an array of filenames
        file_list = [name for name in os.listdir(trialpath) if os.path.isfile(os.path.join(trialpath,name))]
        time.sleep(1)
        if len(file_list) < config['BATCH_SIZE']:
            continue
        
    #import files into usable arrays.

        mean,optimal_tensor = optimal_state_tensor(config,file_list,agent_version)
        
    #optimize:
        obs_v, act_v, _ = zip(*optimal_tensor)
        obs_v = torch.stack(obs_v).reshape((-1,20)) #Reshape the tensor to [B, 20]
        act_v = torch.stack(act_v).reshape((-1))

        optimizer.zero_grad()
        action_scores_v = action_agent.net(obs_v)
        loss_v = objective(action_scores_v,act_v)
        loss_v.backward()
        optimizer.step()
        #print(f"successfully optimized {agent_version+1}")


        agent_version = agent_version + 1
        filepath,trialpath = update_agent_filepath(config,agent_version)
        action_agent.net.save_model(filepath)


        data.append((agent_version,mean,loss_v.item()))
        print(agent_version,mean, loss_v.item())
        data_array = np.array(data)
        np.savetxt(os.path.join(config['agent_path'],'data.csv'), data_array, delimiter=",")
        

 

