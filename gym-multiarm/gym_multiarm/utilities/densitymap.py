import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm
from gym_multiarm.utilities.extractor import extractor

class data_analysis():
    def __init__(self,experiment_dir,data_storage,agent_init,agent_final,output = 'all',type = 'episodes',skip=1):
        self.experiment = experiment_dir
        self.data = data_storage
        self.agent_init = agent_init
        self.agent_final = agent_final
        self.output = output
        self.type = type
        self.skip = skip
        with open(os.path.join(self.data,'config.json')) as file:
            self.config = json.load(file)


    def datacheck(self):
        for i in range(self.agent_init,self.agent_final):
            #check that all expected files exist:
            if os.path.isfile(os.path.join(self.data,self.type,str(i)+'.json')):
                continue
            else:
                if i == self.agent_init:
                    self.agent_init = i+1
                
                else:
                    self.agent_final = i-1
                    break

        print('agent range is',self.agent_init,'to ',self.agent_final)
            


    def extractdata(self):
        #extract useful information out of raw data
        #try:
        try:
            extractor.extract_data(self.agent_init,self.agent_final,self.config,self.data,self.skip,data=self.type)
        except Exception as e:
            print(e,"extractor-error")
            self.datacheck()
    


    def extract_initial_states(self):

        self.target = []
        #self.arm_1 = []#irrelevant when arm 1 always has the same starting conditions
        self.arm_2 = []
        for i in tqdm(range(self.agent_init,self.agent_final,self.skip)):
            agentfile = os.path.join(self.data,self.type,str(i)+".json")
            with open(agentfile,"r") as file:
                episodes = json.load(file)
            for i in range(len(episodes)):
                targetx = episodes[i][1][0][4]
                targety = episodes[i][1][0][5]
                arm_2x = episodes[i][1][0][2]
                arm_2y = episodes[i][1][0][3]
                self.target.append((targetx,targety))
                self.arm_2.append((arm_2x,arm_2y))

    def plot_initial_states(self, lines = True,size=0):
        targetx = []
        targety = []
        arm_2x = []
        arm_2y = []
        
        if size == 0:
            size=len(self.target)
        for i in np.random.choice(range(len(self.target)),size,replace=False): #note: insert a size=int to sample random size
            targetx.append(self.target[i][0])
            targety.append(self.target[i][1])
            arm_2x.append(self.arm_2[i][0])
            arm_2y.append(self.arm_2[i][1])

        fig,ax = plt.subplots()
        plt.scatter(targetx,targety,label = 'target')
        plt.scatter(arm_2x,arm_2y, label = 'arm_2 start')
        if lines == True:
            for i in range(len(arm_2x)):
                plt.plot([targetx[i],arm_2x[i]],[targety[i],arm_2y[i]],'.-')
        
        plt.xlim(-2.2,2.2)
        plt.ylim(-2.2,2.2)
        plt.legend()
        plt.title('Initial States')
        plt.show()



if __name__=="__main__":
    with open("/data/sim/config.json","r") as file:
        config=json.load(file)

    analysis = data_analysis('data/sim','/home/sebastian/Documents/3.0 fixed_1_random_2_repeater',300,320,output='all',type='difficult',skip=1)
    analysis.extractdata()
    analysis.datacheck()
    analysis.extract_initial_states()
    analysis.plot_initial_states(lines=False)

        

