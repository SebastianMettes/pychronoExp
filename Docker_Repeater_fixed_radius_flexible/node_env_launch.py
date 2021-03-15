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
repetitions = config['num_repeat_episodes']
#Setup Environment object
environmentTest = env.Multi_armEnv()
environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],(0,0,1),(0,0,2),pla,config['step_size'],config['max_torque'],[1.0,1.0])

#Create agent object
action_agent = agent(config)

#Modules:
def convert_action(action): #convert 0-8 to [motorA,motorB]
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

    #create the good_episodes, path, for the output data file
    good_episodes = str(host_id)+"."+date_time+".JSON"
    good_episodes = os.path.join(config["save_dir"],str(agent_version),good_episodes)

    #create the bod episodes bath (those which a solution was never found:
    bad_episodes = str(host_id)+'.'+date_time+".JSON"
    bad_episodes = os.path.join(config["difficult_dir"],str(agent_version),bad_episodes)

    #Create cold starge data path:
    ##cold_storage = os.path.join(config["cold_storage"],str(host_id)+'.'+date_time+'.JSON')

    #set the target from random coordinates:
    target_angle = (random.random()*2*math.pi)
    target_radius = random.random()*2*arm_length
    target = [target_radius*math.sin(target_angle),target_radius*math.cos(target_angle)]

    #now find two random starting positions for the arm.
    #note they must still both be "arm length" in length (from config file):
    #note, the plane of operation is the X-Z Plane (X,y,Z)
    #position 1:
    #pos1_angle = (random.random()*2*math.pi)\
    pos1_angle = 0
    position1 = (arm_length*math.cos(pos1_angle),0,arm_length*math.sin(pos1_angle))

    #position 2:
    pos2_angle = (random.random()*math.pi)
    position2 = (arm_length*math.cos(pos2_angle),0,arm_length*math.sin(pos2_angle))

    position2 = (position1[0]+position2[0],0,position1[2]+position2[2])
    reward_list = []
    j = 0
    k=0
    multi_state_tensor = []
    while j<repetitions:
    #reset the environment to starting state
        print("environment Reset, attempt #",j+1)
        state_tensor = []
        environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],position1,position2,pla,config['step_size'],config['max_torque'],target)
   


        #get initial state 
        state_new = environmentTest.getstate()
        state_init = state_new
        reward_total = 0
         #initialize an empty state tensor

        #conduct simulation
        for i in range(numSteps):
            #environmentTest.render() #not applicable to slave machines.
            action_digit = action_agent.calc_action(agent_version,state_new) #use agent to determine action from current state and agent version
            action = convert_action(action_digit)
            state,state_new,action = environmentTest.forwardStep([action[0],action[1]]) #run simulation
            reward = environmentTest.reward(config) #calculate reward
            reward_total = reward+reward_total
            state_tensor.append((state,state_new,action_digit,reward)) #append information to state_tensor

            if environmentTest.headless ==False:
                environmentTest.render()
        
        multi_state_tensor.append(state_tensor)
        reward_list.append(reward_total)
        j=j+1
        max_reward = max(reward_list)
        if max_reward <0:
            k=k+1
            print('sub-zero reward, extra attempt #',k+1)
            j=j-1
            if k>10*repetitions:
                j=repetitions
                with open(bad_episodes,"w") as file:
                    max_index = reward_list.index(max(reward_list))
                    state_tensor = multi_state_tensor[max_index]
                    file.write(json.dumps(state_tensor,indent=0)) #save state_tensor for agent optimization
                    print('saved difficult episode')

    #with open(cold_storage,"w") as file:        
    #    file.write(json.dumps(multi_state_tensor,indent=0)) 
    #    print('saved data to cold storage')
    max_index = reward_list.index(max(reward_list))
    print(max_index,reward_list[max_index],len(reward_list),'index, value, length')
    state_tensor = multi_state_tensor[max_index]
    j=j+1

    if max_reward>0:
        with open(good_episodes,"w") as file:
            file.write(json.dumps(state_tensor,indent=0)) #save state_tensor for agent optimization
            print("Successful episode Saved, agent version # ", agent_version)

        


