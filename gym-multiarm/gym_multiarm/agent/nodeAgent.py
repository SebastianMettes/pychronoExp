import os
import json
from gym_multiarm.neural_network.network import cross_entropy_agent 
import torch
import torch.nn as nn
import numpy as np
class agent():
    def __init__(self,agent_config):
        self.agent_config = agent_config
        self.HIDDEN_SIZE = agent_config['HIDDEN_SIZE']
        self.OBSERVE_SIZE = agent_config['OBSERVE_SIZE']
        self.N_ACTIONS = agent_config['N_ACTIONS']
        self.BATCH_SIZE = agent_config['BATCH_SIZE']
        self.PERCENTILE = agent_config['PERCENTILE']    
        self.agent_path = agent_config['agent_path']

        self.net = cross_entropy_agent(self.OBSERVE_SIZE,self.HIDDEN_SIZE,self.N_ACTIONS)
        if os.path.isfile(os.path.join(self.agent_path,str(1),'model.pt')):
            self.update_version()

    def calc_action(self,agent_version,state):
        #check that version is the most recent OR requested version
        if self.version != agent_version:
            self.net.load_model(os.path.join(self.agent_path,str(agent_version),'model.pt'))
        

        #calculate action probabilities
        action_probability = self.net.forward(torch.FloatTensor([state]))
        action_probability = nn.Softmax(action_probability)
        action_probability = action_probability.data.numpy()[0]
        action = np.random.choice(len(action_probability),p=action_probability)
        
        return [action] #return action (should be a number between 0 and 8)

    def update_version(self):#determine most recent agent release folder 
        i = 1
        while os.path.isdir(os.path.join(self.agent_path,str(i))):
            i+=1
        i -=1 
        self.version = i
        self.net.load_model(os.path.join(self.agent_path,str(i),'model.pt'))
        return(i)


    

#class DLAgent(agent):
#    def __init__(self):
#        super().__init__()


#    def normalize_action(self, action):
#        return normalize(action)

#    def calc_action(self,state):
        #call DL network on state
#        action  = self.normalize_action(self.network(state))
#        return action
    
#    def update_version(self):
#        pass

#class BAgent(agent):
#    pass

#class QAgent(agent):
#    def __init__(self):
#        pass


#def doagentstuff(a:agent):
#    a.calc_action(s)
#    a.update_version()

#dlagent = DLAgent()

#doagentstuff(dlagent)

#qagent = QAgent()

#doagentstuff(qagent)

#bb = BAgent()

#bb.cal