from gym_multiarm.envs import multi_arm_env as env
from agent.DLAgent import calc_action, update_agent
from datetime import datetime
import random
import math
import csv
import socket
import numpy as np
import json
import os
import uuid

#Setup Environment
#import config file

host_id = uuid.uuid4()

#load config.json here... 
with open("/data/sim/config.json","r") as file:
    config=json.load(file)


#steel = env.Multi_armMaterial("steel",2.15E9,0.5,8050)
steelprop = config['materials']['steel']
steel = env.Multi_armMaterial('steel',steelprop['E'],steelprop['poisson'],steelprop['density'])
plaprop = config['materials']['pla']
pla = env.Multi_armMaterial('pla',plaprop['E'],plaprop['poisson'],plaprop['density'])

arm_length = config['dimensions']["arm_length"]
numSteps = config['num_steps']

environmentTest = env.Multi_armEnv()
environmentTest.reset(False,True,config['dimensions']['arm_width'],config['dimensions']['arm_height'],arm_length,arm_length,steel,config['step_size'],config['max_torque'],[1.0,1.0])




while True:
    #check for new weights
    agent_id = update_agent()
    state_tensor = []
    #set the target from random coordinates:
    target_angle = (random.random()*2*math.pi)
    target_radius = random.random()*2*arm_length
    target = [target_radius*math.sin(target_angle),target_radius*math.cos(target_angle)]
    environmentTest.reset(False,True,0.2,0.125,1.0,1.0,pla,0.001,1,target)
    state = environmentTest.getstate()
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    filename = str(host_id)+"."+date_time+".JSON"
    filename = os.path.join(config["save_dir"],"trial",agent_id,filename)
    for i in range(numSteps):
        #environmentTest.render()
        action = calc_action(agent_id,state_tensor) 
        state,state_new,action = environmentTest.forwardStep([action[0],action[1]])
        reward = environmentTest.reward()
        state_tensor.append((state,state_new,action,reward))
    
    with open(filename,"w") as file:
        file.write(json.dumps(state_tensor,indent=0))
        print("File Saved")
    


