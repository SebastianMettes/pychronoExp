import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm


#Select agent of interest
agent = 131
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
        episodes.append((sum(rewards),states))  


reward_cutoff = np.percentile(rewards,config["PERCENTILE"],overwrite_input=True)
episodes = list(filter(lambda x: x[0] >= reward_cutoff,episodes))


data = []
#extract x,y coordinate data
for i in tqdm(range(len(episodes))):
    EpisodeX = []
    print(i)
    for j in range(0,config["num_steps"]):
        posX = episodes[i][1][j][6]
        posY = episodes[i][1][j][7]
        EpisodeX.append((posX,posY))
    data.append(EpisodeX)

plt_data = data[0]
xcoords,ycoords = zip(*plt_data)

plt.figure()
plt.plot(xcoords,ycoords)
plt.show()





#graph coordinate date

#