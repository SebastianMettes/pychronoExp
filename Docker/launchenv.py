from gym_multiarm.envs import multi_arm_env as env
from agent.DLAgent import agent
from datetime import datetime
import random
import math
import csv
import socket
import numpy as np
import json
import os
import uuid


##Create a unique ID for host computer
host_id = uuid.uuid4()

##load config.json here... 
with open("/data/sim/config.json","r") as file:
    config=json.load(file)

##Import materials
steelprop = config['materials']['steel']
steel = env.Multi_armMaterial('steel',steelprop['E'],steelprop['poisson'],steelprop['density'])
plaprop = config['materials']['pla']
pla = env.Multi_armMaterial('pla',plaprop['E'],plaprop['poisson'],plaprop['density'])

##set arm length (all arms are identical)
arm_length = config['dimensions']["arm_length"]

##set number of simulation steps per simulation
numSteps = config['num_steps']

#Setup Environment object
environmentTest = env.Multi_armEnv()
environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],arm_length,arm_length,steel,config['step_size'],config['max_torque'],[1.0,1.0])

#Create agent object
action_agent = agent()


while True:
    #check for new weights
    agent_version = action_agent.update_version(config["agent_path"])

    state_tensor = [] #initialize an empty state tensor

    #set the target from random coordinates:
    target_angle = (random.random()*2*math.pi)
    target_radius = random.random()*2*arm_length
    target = [target_radius*math.sin(target_angle),target_radius*math.cos(target_angle)]

    #reset the environment to starting state
    environmentTest.reset(False,True,0.2,0.125,1.0,1.0,pla,0.001,1,target)

    #get initial state 
    state = environmentTest.getstate()

    #get the time as part of the unique output data file.
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")

    #create the filename, path, for the output data file
    filename = str(host_id)+"."+date_time+".JSON"
    filename = os.path.join(config["save_dir"],str(agent_version),filename)

    #conduct simulation
    for i in range(numSteps):
        #environmentTest.render() #not applicable to slave machines.
        action = action_agent.calc_action(agent_version,state_tensor) #use agent to determine action from current state and agent version
        state,state_new,action = environmentTest.forwardStep([action[0],action[1]]) #run simulation
        reward = environmentTest.reward() #calculate reward
        state_tensor.append((state,state_new,action,reward)) #append information to state_tensor
    
    with open(filename,"w") as file:
        file.write(json.dumps(state_tensor,indent=0)) #save state_tensor for agent optimization
        print("File Saved")
    


