import os
class agent():
    def __init__(self):
        pass

    def calc_action(self,agent_version,state):
        #Will need to receive complete state data (state)
        #receive agent ID value for Deep Network weights
        #check for updates

        return [1,1] #return action

    def update_version(self,agent_path):#determine most recent agent release folder 
        i = 1
        while os.path.isdir(os.path.join(agent_path,str(i))):
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