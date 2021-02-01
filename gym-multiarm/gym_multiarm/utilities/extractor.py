import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm


class extractor():
    def __init__(self,agent_number,agent_final,config,local_dir,skip = 1):
        agent_init = agent_number
        agent_final = agent_final
        config = config

        for i in range(agent_init,agent_final,skip):
            agent = i
            episodes = []

            #set location of data
            trialpath = os.path.join(config['save_dir'],str(agent))
            file_list = [name for name in os.listdir(trialpath) if os.path.isfile(os.path.join(trialpath,name))]

            #select episodes 
            for i in tqdm(range(0,len(file_list))):
                with open(os.path.join(config['save_dir'],str(agent),file_list[i])) as file:
                    state_tensor = json.load(file)
                    states, _, actions, rewards = zip(*state_tensor)
                    states_position = []
                    for i in range(len(states)):
                        #link 1 position x, y, link 2 pos x, y, target x,y,action 0, action 1
                        temp = [states[i][0],states[i][1],states[i][6],states[i][7],states[i][18],states[i][19],states[i][14],states[i][17]]
                        states_position.append(temp)

                    episodes.append((sum(rewards),states_position))  

            rewards, _ = zip(*episodes)
            reward_cutoff = np.percentile(rewards,config['PERCENTILE'],overwrite_input=True)
            episodes = list(filter(lambda x: x[0] >= reward_cutoff,episodes))
            episodes = sorted(episodes,key=lambda x: x[0])

            filename = os.path.join(local_dir,str(agent)+".json")
            with open(filename,"w") as file:
                file.write(json.dumps(episodes,indent=0)) #save state_tensor for agent optimization


if __name__=="__main__":
    with open("/data/sim/config.json","r") as file:
        config=json.load(file)

    extractor(1,303,config,'/home/sebastian/Documents/random_starts/episodes',skip=3)

