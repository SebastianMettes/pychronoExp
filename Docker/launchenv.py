try:
    from gym_multiarm.envs import multi_arm_env as env
    print("successfully imported env")
except:
    print("fail to import env")
    exit()
try:
    from agent.DLAgent import calc_action, agent_name, update_agent
    print("successfully imported agent")
except:
    print("fail to import agent")
    exit()
from datetime import datetime
import random
import math
import csv
import socket
import numpy as np
import json

#Setup Environment
steel = env.Multi_armMaterial("steel",2.15E9,0.5,8050)
pla = env.Multi_armMaterial("pla",2.3E7,0.5,1240)
arm_length = 1.1
numSteps = 3000
environmentTest = env.Multi_armEnv()
environmentTest.reset(False,True,3,0.02,0.0125,arm_length,arm_length,steel,0.001,1,[1.0,1.0])

hostName = socket.gethostname()


while True:
    state_tensor = []
    target_angle = (random.random()*2*math.pi)
    target_radius = random.random()*2*arm_length
    target = [target_radius*math.sin(target_angle),target_radius*math.cos(target_angle)]
    environmentTest.reset(False,True,3,0.2,0.125,1.0,1.0,pla,0.001,1,target)
    state = environmentTest.getstate()
    now = datetime.now()
    date_time = now.strftime("%Y%m%d%H%M%S")
    agentName = agent_name()
    filename = agentName+"."+hostName+"."+date_time+".csv"
    for i in range(numSteps):
        #environmentTest.render()
        action = calc_action()
        state,state_new,action = environmentTest.forwardStep([action[0],action[1]])
        reward = environmentTest.reward()
        state_tensor.append((state,state_new,action,reward))
    
    with open(filename,"w") as file:
        file.write(json.dumps(state_tensor,indent=4))
        print("File Saved")
    


