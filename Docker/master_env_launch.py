import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import os
import os.path
import json
from gym_multiarm.agent.nodeAgent import agent
from gym_multiarm.envs import multi_arm_env as env
import time
import numpy as np


##load config.json  
with open("/data/sim/config.json","r") as file:
    config=json.load(file)

batch_size = config["gpu_batch_size"]

#Create agent object and related components
action_agent = agent(config)
objective = nn.CrossEntropyLoss()
optimizer = optim.Adam(params = action_agent.net.parameters(),lr = config['learning_rate'])
sm = nn.Softmax(dim=1)

#OUTPUT DATA ARRAY
##Check if previous version exists:
data = []
try:
    data = np.loadtxt(os.path.join(config['agent_path'],'data.csv'),delimiter = ',')
    #print(data)
except Exception as e:
    print('could not load data.csv', e)
    with open(os.path.join(config['agent_path'],'data.csv'),'w') as file: 
        pass



#modules:
def update_optimizer(action_agent,config,agent_version):#determine most recent agent release folder 
    i = agent_version
    filepath,_,_,_=update_agent_filepath(config,i)
    print(filepath)
    
    print('loaded agent',i)
    action_agent.net.load_model(os.path.join(filepath,'model.pt'))
    action_agent.cuda()
    optimizer = optim.Adam(params=action_agent.net.parameters(),lr=config['learning_rate'])
    optimizer.load_state_dict(torch.load(os.path.join(filepath,'optimizer.pt')))
        
    return(i,optimizer,action_agent)
    
def update_agent_filepath(config,agent_version):
    filepath = os.path.join(config["agent_path"],str(agent_version))
    i=0
    paththere = True
    while paththere == True:
        if os.path.isdir(os.path.join(config["agent_path"],str(agent_version+i+1))) == True:
            filepath = os.path.join(config["agent_path"],str(agent_version+i+1))
            print('agent version is currently',i+1)
            i=i+1
        else:
            filepath = os.path.join(config["agent_path"],str(agent_version+i))
            agent_version = agent_version+i
            paththere = False

        
    trialpath = os.path.join(config["save_dir"],str(agent_version))
    if os.path.isdir(trialpath) == False:
        os.mkdir(trialpath)
        os.system(f"chmod 777 {trialpath}")
    difficultpath = os.path.join(config["difficult_dir"],str(agent_version))
    if os.path.isdir(difficultpath) == False:
        os.mkdir(difficultpath)
        os.system(f"chmod 777 {difficultpath}")

    return(filepath,trialpath,agent_version,difficultpath)

def optimal_state_tensor(config,file_list,agent_version):
    episodes = []

    for i in range(0,len(file_list)):
        #print(os.path.join(config['save_dir'],str(agent_version),file_list[i]))
        with open(os.path.join(config['save_dir'],str(agent_version),file_list[i])) as file:
            state_tensor = json.load(file)
            states, _, actions, rewards = zip(*state_tensor)
            state_tensor = (
                torch.FloatTensor(states),
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

filepath,trialpath,agent_version,difficult_path = update_agent_filepath(config,agent_version)

print("the current agent is", agent_version)

#check if any newer agent_version exist:

if agent_version >1:
    agent_version,optimizer,action_agent = update_optimizer(action_agent,config,agent_version)
    filepath,trialpath,agent_version,difficult_path = update_agent_filepath(config,agent_version)
    print(filepath,trialpath,difficult_path)
if agent_version == 1:
    action_agent.net.save_model(filepath,optimizer)
action_agent.cuda()

print("I'm here now...", filepath)    

while True:

#Load in the config file, save the material property values.
    with open("/data/sim/config.json","r") as file:
        config=json.load(file)
    plaprop = config['materials']['pla']
    pla = env.Multi_armMaterial('pla',plaprop['E'],plaprop['poisson'],plaprop['density'])

#Continuously check for new json files with complete state tensors for each episode
    #create an array of filenames
    file_list = [name for name in os.listdir(trialpath) if os.path.isfile(os.path.join(trialpath,name))]
    time.sleep(1)
    if len(file_list) < config['BATCH_SIZE']:
        continue
    print(agent_version)
    
#import files into usable arrays.

    mean,optimal_tensor = optimal_state_tensor(config,file_list,agent_version)
    
    if len(optimal_tensor) < batch_size:
        raise ValueError("Tensor Size was less than batch size! -- ")
    
    t = len(optimal_tensor)/batch_size

    loss_store = []

    print("And now here...")
    for i in range(0,int(t)):
        print("Running a batch from",batch_size*i,'to',batch_size*(i+1) - 1)
        optimal_tensor_batch = optimal_tensor[batch_size*i:(batch_size*(i+1) - 1)]
        #optimize:
        obs_v, act_v, _ = zip(*optimal_tensor_batch)
        obs_v = torch.stack(obs_v).reshape((-1,config["OBSERVE_SIZE"])).cuda() #Reshape the tensor to [B, observation size]
        act_v = torch.stack(act_v).reshape((-1)).cuda()
        optimizer.zero_grad()
        action_scores_v = action_agent.net(obs_v)
        loss_v = objective(action_scores_v,act_v)
        loss_v.backward()
        optimizer.step()
        loss_store.append(loss_v.detach().cpu().item()) 
        #print(loss_store)
    
    #optimal_tensor_batch = optimal_tensor[batch_size*int(t):]
    #optimize remaining:
    #obs_v, act_v, _ = zip(*optimal_tensor)
    #obs_v = torch.stack(obs_v).reshape((-1,20)).cuda() #Reshape the tensor to [B, 20]
    #act_v = torch.stack(act_v).reshape((-1)).cuda()
    #optimizer.zero_grad()

    #backwards
    #action_scores_v = action_agent.net(obs_v)
    #loss_v = objective(action_scores_v,act_v)
    #loss_v.backward()
    #optimizer.step()
    #print(f"successfully optimized {agent_version+1}")


    agent_version = agent_version + 1
    filepath,trialpath,agent_version,difficult_path = update_agent_filepath(config,agent_version)
    action_agent.cpu()
    action_agent.net.save_model(filepath,optimizer)
    action_agent.cuda()
    loss_mean = np.mean(loss_store)

    data = list(data)
    data.append((agent_version,mean,loss_mean))
    print(agent_version,mean, loss_mean)
    data_array = np.array(data)
    np.savetxt(os.path.join(config['agent_path'],'data.csv'), data_array, delimiter=",")
    print('data saved')