from gym_multiarm.envs import multi_arm_env as env
from gym_multiarm.agent.nodeAgent import agent
from datetime import datetime
import random
import math
import csv
import socket
import numpy as np
import json
import os
import uuid
#notes:
'''
To launch the agent,the config file must include all environment and agent parameters.

'''

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
environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],arm_length,arm_length,pla,config['step_size'],config['max_torque'],[1.0,1.0])

#Create agent object
action_agent = agent(config)

#Modules:
def convert_action(action): #convert 0-7 to [motorA,motorB]
    if action == 0:
        action = [0,0]
    elif action == 1:
        action = [1,0]
    elif action == 2:
        action = [0,1]
    elif action == 3:
        action = [1,1]
    elif action == 4:
        action = [-1,0]
    elif action == 5:
        action = [0,-1]
    elif action == 6:
        action = [-1,-1]
    elif action == 7:
        action = [-1,1]
    elif action == 8:
        action = [1,-1]
    else:
        print('action state error')
    return(action)
    
while True:

    #get the time as part of the unique output data file.
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")

    #check for new agent version:

    agent_version = action_agent.update_version()

    #create the filename, path, for the output data file
    filename = str(host_id)+"."+date_time+".JSON"
    filename = os.path.join(config["save_dir"],str(agent_version),filename)

    #set the target from random coordinates:
    target_angle = (random.random()*2*math.pi)
    target_radius = random.random()*2*arm_length
    target = [target_radius*math.sin(target_angle),target_radius*math.cos(target_angle)]

    #reset the environment to starting state
    environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],arm_length,arm_length,pla,config['step_size'],config['max_torque'],target)
  

    #get initial state 
    state_new = environmentTest.getstate()

    state_tensor = [] #initialize an empty state tensor

    #conduct simulation
    for i in range(numSteps):
        #environmentTest.render() #not applicable to slave machines.
        action_digit = action_agent.calc_action(5,state_new) #use agent to determine action from current state and agent version
        print(action_digit)
        action = convert_action(action_digit)
        state,state_new,action = environmentTest.forwardStep([action[0],action[1]]) #run simulation
        reward = environmentTest.reward() #calculate reward
        state_tensor.append((state,state_new,action_digit,reward)) #append information to state_tensor
    
    with open(filename,"w") as file:
        file.write(json.dumps(state_tensor,indent=0)) #save state_tensor for agent optimization
        print("File Saved")
    


