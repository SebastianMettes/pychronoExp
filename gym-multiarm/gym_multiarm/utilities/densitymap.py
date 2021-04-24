import matplotlib.pyplot as plt
import numpy as np
import os
import json
from tqdm.auto import tqdm
from gym_multiarm.utilities.extractor import extractor
import math
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

class data_analysis():
    def __init__(self,experiment_dir,data_storage,agent_init,agent_final,output = 'all',etype = 'episodes',skip=1):
        self.experiment = experiment_dir
        self.data = data_storage
        self.agent_init = agent_init
        self.agent_final = agent_final
        self.output = output
        self.etype = etype
        self.skip = skip
        with open(os.path.join(self.data,'config.json')) as file:
            self.config = json.load(file)


    def datacheck(self):
        for i in range(self.agent_init,self.agent_final):
            #check that all expected files exist:
            if os.path.isfile(os.path.join(self.data,self.etype,str(i)+'.json')):
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
            extractor.extract_data(self.agent_init,self.agent_final+1,self.config,self.data,self.skip,data=self.etype)
        except Exception as e:
            print(e,"extractor-error")
            self.datacheck()
    


    def extract_initial_states(self):

        self.target = []
        #self.arm_1 = []#irrelevant when arm 1 always has the same starting conditions
        self.arm_2 = []
        self.rewards = []
        self.distance = []
        self.distance_zero = []
        for i in tqdm(range(self.agent_init,self.agent_final+1,self.skip)):
            agentfile = os.path.join(self.data,self.etype,str(i)+".json")
            with open(agentfile,"r") as file:
                episodes = json.load(file)
            for i in range(len(episodes)):
                targetx = episodes[i][1][0][4]
                targety = episodes[i][1][0][5]
                arm_2x = episodes[i][1][0][2]
                arm_2y = episodes[i][1][0][3]
                self.target.append((targetx,targety))
                self.arm_2.append((arm_2x,arm_2y))
                self.rewards.append((episodes[i][0]))
                distance = math.sqrt((targetx-arm_2x)**2+(targety-arm_2y)**2)
                distance_z = math.sqrt((targetx-1.1)**2+(targety)**2)
                self.distance.append(distance)
                self.distance_zero.append(distance_z)
                
        biglist = zip(self.rewards,self.arm_2,self.target)
        biglist = sorted(biglist,key = lambda x: x[0])
        self.rewards,self.arm_2,self.target = zip(*biglist)
        

            
        #sort the list by episode reward:

        


        #rearrange increasing rewards order:

    def plot_initial_states(self, buckets, label, lines = True,size=0,):

        
        if size == 0:
            size=len(self.target)

        fig,ax = plt.subplots()
        #for i in np.random.choice(range(len(self.target)),size,replace=False): #note: insert a size=int to sample random size
        for i in range(buckets):
            targetx = []
            targety = []
            arm_2x = []
            arm_2y = []
            reward = []      
            print(i)      
            for j in range(int(i*(len(self.target)/buckets)),int((i+1)*((len(self.target)/buckets)))-1):
                print(j)
                targetx.append(self.target[j][0])
                targety.append(self.target[j][1])
                arm_2x.append(self.arm_2[j][0])
                arm_2y.append(self.arm_2[j][1])
                reward.append(self.rewards[j])

            reward_avg = np.average(reward)
            plt.scatter(targetx,targety,label = 'target')
            plt.scatter(arm_2x,arm_2y, label = 'end_effector init. pos.')
            plt.title(str(i*(100/buckets))+'th'+' to '+str((1+i)*(100/buckets))+'th percentile' + ' avg. reward '+str(reward_avg))
            if lines == True:
                for k in range(len(arm_2x)):
                    plt.plot([targetx[k],arm_2x[k]],[targety[k],arm_2y[k]],'--',color='silver')
            
            plt.xlim(-2.2,2.2)
            plt.ylim(-2.2,2.2)
            plt.legend()
            plt.subplots()



        #plt.title('Initial States')
        plt.show()

    def reward_histogram(self,agent_list):
        def CDF(data):
            return np.sort(data), np.linspace(0,1,len(data),endpoint=False)

        for i in range(len(agent_list)):
            historewardlist = []
            steps = []
            j=0
            agentfile = os.path.join(self.data,self.etype,str(agent_list[i])+".json")
            with open(agentfile,"r") as file:
                episodes = json.load(file)
                for k in range(len(episodes)):
                    historewardlist.append(episodes[k][0])
                    steps.append(j)
                    j=j+1


            plt.plot(*CDF(historewardlist),label = 'rewards agent '+str(agent_list[i]),)
            #plt.plot(steps,historewardlist, label = 'rewards agent '+str(agent_list[i]))
            #plt.legend()
        plt.title('CDF - agent rewards '+str(agent_list[0])+' through '+str(agent_list[len(agent_list)-1]))
        plt.legend()
        plt.xlabel('Reward')
        plt.ylabel("Density")
        plt.show()

    def path_plot(self,agent_list,episode_list):
        for i in range(len(agent_list)):
            fig,ax=plt.subplots()
            plt.xlim(-2.2,2.2)
            plt.ylim(-2.2,2.2)
            with open(os.path.join(self.data,self.etype,str(agent_list[i])+'.json')) as file:
                episodes = json.load(file)
                rewards, _ = zip(*episodes)
            for j in range(len(episode_list)):
                #extract x,y data from arm 1:
                arm1 = []
                arm2 = []
                action = []
                for k in range(self.config['num_steps']):
                    posX = episodes[episode_list[j]][1][k][2]
                    posY = episodes[episode_list[j]][1][k][3]
                    arm1.append((posX,posY))

                #extract x,y data from arm 2:
                for k in range(self.config['num_steps']):
                    posX = episodes[episode_list[j]][1][k][0]
                    posY = episodes[episode_list[j]][1][k][1]
                    arm2.append((posX,posY))
                
                #extract x,y data from arm 2:
                for k in range(self.config['num_steps']):
                    action0 = episodes[episode_list[j]][1][k][6]
                    action1 = episodes[episode_list[j]][1][k][7]
                    action.append((posX,posY))

                targetx = episodes[episode_list[j]][int(1)][int(0)][int(4)]
                targety = episodes[episode_list[j]][int(1)][int(0)][int(5)]

                xcoords,ycoords = zip(*arm1)
                plt.plot(xcoords,ycoords,label='epi '+str(episode_list[j])+' r '+"{:.2f}".format(rewards[episode_list[j]]))
                #xcoords,ycoords = zip(*arm2)
                #plt.plot(xcoords,ycoords)
                try:
                    circle1 = plt.Circle((targetx, targety), self.config['reward_radius'], color='r')
                except:
                    circle1 = plt.Circle((targetx, targety), 0.05, color='r')
                circle2 = plt.Circle((arm1[0][0],arm1[0][1]),0.05,color='g')
                ax.add_patch(circle1)
                ax.add_patch(circle2)
                plt.legend()
                plt.title('paths of agent #'+str(agent_list[i]))
                plt.xlabel
            plt.show()

        



        pass


    def loss_plot(self,vertical = False):

        lossdata = os.path.join(os.path.join(self.data,'data.csv'))
        csvf = np.loadtxt(lossdata,delimiter = ',')
        Aversion,avgReward,loss = zip(*csvf)
        plt.plot(Aversion,avgReward)
        plt.title("Reward")
        if vertical == True:
            lines = [232,240,251,270,406,508,648,691,744,765,774,845,981,996,1125,1153,1173,1257,1392,1434,1498,1618]
            for i in range(len(lines)):
                plt.axvline(x = lines[i], ymin = 0,c='r')
        plt.subplots()
        plt.title('Loss')
        plt.plot(Aversion,loss)
        if vertical == True:
            lines = [232,240,251,270,406,508,648,691,744,765,774,845,981,996,1125,1153,1173,1257,1392,1434,1498,1618]
            for i in range(len(lines)):
                plt.axvline(x = lines[i], ymin = 0,c='r')
        plt.show()

    def distance_plot(self):
        model = LinearRegression()
        model.fit(np.array(self.distance)[:,np.newaxis],self.rewards)
        print(model.coef_)
        print(model.intercept_)

        plt.scatter(self.distance,self.rewards)
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals_pred = model.intercept_+model.coef_*(x_vals)
        r2 = r2_score(self.rewards,model.intercept_+model.coef_*(self.distance))
        plt.plot(x_vals,y_vals_pred,'--')
        plt.title("Distance to Target vs. Total Reward, linear fit r^2 =  "+str(round(r2,3)))
        plt.show()

    def distance_zero_plot(self):
        model = LinearRegression()
        model.fit(np.array(self.distance_zero)[:,np.newaxis],self.rewards)
        print(model.coef_)
        print(model.intercept_)

        plt.scatter(self.distance_zero,self.rewards)
        axes = plt.gca()
        x_vals = np.array(axes.get_xlim())
        y_vals_pred = model.intercept_+model.coef_*(x_vals)
        r2 = r2_score(self.rewards,model.intercept_+model.coef_*(self.distance_zero))
        plt.plot(x_vals,y_vals_pred,'--')
        plt.title("Distance to Target vs. Total Reward, linear fit r^2 =  "+str(round(r2,3)))
        plt.show()



if __name__=="__main__":
    #with open("/data/sim/config.json","r") as file:
    #    config=json.load(file)

    analysis = data_analysis('data/sim','/home/sebastian/Documents/5.4 Flexible',1650,1656,output='all',etype='episodes',skip=1)
    
    #analysis.extractdata()
    analysis.datacheck()
    analysis.extract_initial_states()
    analysis.plot_initial_states(buckets=5,label = '',lines=False)
    #analysis.distance_plot()
    #analysis.distance_zero_plot()
    #analysis.reward_histogram([250,647,773,1124,1391,1617,1710])
    #analysis.path_plot([1710],[0,50,100,150,200,250,300]) 
    #analysis.loss_plot(vertical=True)   

