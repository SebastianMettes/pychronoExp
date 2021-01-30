import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm


agent_init = 21
agent_final = 22
folder = "random_starts"

for i in range(agent_init,agent_final):
    agent = i
    episodes = []

    #import the config file
    with open("/data/sim/config.json","r") as file:
        config=json.load(file)

    #set location of data
    trialpath = os.path.join("/data/sim/trial",str(agent))

    file_list = [name for name in os.listdir(trialpath) if os.path.isfile(os.path.join(trialpath,name))]
    #select episodes 
    for i in tqdm(range(0,len(file_list))):
        with open(os.path.join(config['save_dir'],str(agent),file_list[i])) as file:
            state_tensor = json.load(file)
            states, _, actions, rewards = zip(*state_tensor)
            states_position = []
            for i in range(len(states)):
                temp = [states[i][0],states[i][1],states[i][6],states[i][7],states[i][18],states[i][19]]
                states_position.append(temp)

            episodes.append((sum(rewards),states_position))  


    filename = os.path.join("/home/sebastian/Documents",folder,str(agent)+".json")
    with open(filename,"w") as file:
        file.write(json.dumps(episodes,indent=0)) #save state_tensor for agent optimization


    print(filename)