import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm



agent = 17
episode_number = 90
percentile = 70
num_steps = 10000
filename = os.path.join("/home/sebastian/Documents",str(agent)+".json")

with open(filename,"r") as file:
    episodes =json.load(file) #save state_tensor for agent optimization

rewards, _ = zip(*episodes)
reward_cutoff = np.percentile(rewards,percentile,overwrite_input=True)
episodes = list(filter(lambda x: x[0] >= reward_cutoff,episodes))
episodes = sorted(episodes,key=lambda x: x[0])


data = []
#extract x,y coordinate data
for i in tqdm(range(len(episodes))):
    EpisodeX = []
    print(i)
    for j in range(0,num_steps):
        posX = episodes[i][1][j][2]
        posY = episodes[i][1][j][3]
        EpisodeX.append((posX,posY))
    data.append(EpisodeX)
data1 = []
#extract x,y coordinate data
for i in tqdm(range(len(episodes))):
    EpisodeX = []
    print(i)
    for j in range(0,num_steps):
        posX = episodes[i][1][j][0]
        posY = episodes[i][1][j][1]
        EpisodeX.append((posX,posY))
    data1.append(EpisodeX)

plt_data = data[0]
plt_data1 = data1[0]
xcoords,ycoords = zip(*plt_data)
xcoords1,ycoords1 = zip(*plt_data1)

fig,ax = plt.subplots()

targetx = episodes[episode_number][int(1)][int(0)][int(4)]
targety = episodes[episode_number][int(1)][int(0)][int(5)]
plt.plot(xcoords,ycoords)
plt.plot(xcoords1,ycoords1)
plt.title(f"Episode {episode_number} -- Reward : {episodes[episode_number][0]}")
circle1 = plt.Circle((targetx, targety), 0.01, color='r')
ax.add_patch(circle1)

plt.show()

