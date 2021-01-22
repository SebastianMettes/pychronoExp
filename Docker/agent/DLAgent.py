import os
import torch
import json

class agent():
    def __init__(self,agent_path):
        self.agent_path = agent_path
        pass

    def calc_action(self,agent_version,state):
        #Pull weights for network
        with open(os.path.join(self.agent_path,str(agent_version),"weights.json"),"r") as file:
            weights=json.load(file)

        return [1,1] #return action

    def update_version(self):#determine most recent agent release folder 
        i = 1
        while os.path.isdir(os.path.join(self.agent_path,str(i))):
            i+=1
        i -=1 
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