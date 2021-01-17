import gym
import pychrono as chrono
import pychrono.fea as fea
import pychrono.mkl as mkl
try: 
    import pychrono.irrlicht as chronoirr
except:
    print('only headless mode supported')
    pass
import time
import random
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
try: 
    from gym_multiarm.envs.packages import multi_arm_assembler_3 as sim
except:
    pass
#try:
#    from packages import multi_arm_assembler_3 as sim
#except:
#    pass

class Multi_armMaterial():
    def __init__(self,name, modulus, poisson, density):
        self.name = name
        self.modulus = modulus
        self.poisson = poisson
        self.density = density
        self.shear = self.poisson*self.modulus

class Multi_armEnv(gym.Env):
    metadata = {'render.modes':['human']}

    def __init__(self):
        self.state = []
    
    def getstate(self): #determine state of the arm 
        arm1Pos = self.arm1.arm_tip.GetPos()
        arm2Pos = self.arm2.arm_tip.GetPos()
        arm1Vel = self.arm1.arm_tip.GetPos_dt()
        arm2Vel = self.arm2.arm_tip.GetPos_dt()
        arm1Acc = self.arm1.arm_tip.GetPos_dtdt()
        arm2Acc = self.arm2.arm_tip.GetPos_dtdt()
        motor1Pos = self.arm1.motor.GetMotorRot()
        motor2Pos = self.arm2.motor.GetMotorRot()
        motor1Vel = self.arm1.motor.GetMotorRot_dt()
        motor2Vel = self.arm2.motor.GetMotorRot_dt()

        self.state_new = [arm1Pos.x,arm1Pos.y,arm1Vel.x,arm1Vel.y,arm1Acc.x,arm1Acc.y,arm2Pos.x,arm2Pos.y,arm2Vel.x,arm2Vel.y,arm2Acc.x,arm2Acc.y,motor1Pos,motor1Vel,self.mtorque[0],motor2Pos,motor2Vel,self.mtorque[1],self.target[0],self.target[1]]
        
    def reset(self,saveoutput,headless,maxtime,crossx,crossy,length1,length2,material,timestep,maxtorque,target):
        #Check input information:
        if len(target) != 2:
            print("Target is list of length 2, [x,y] coordinates")
            quit()
        self.target=target
        self.material = material
        self.length1=length1
        self.length2 = length2
        self.crossx=crossx
        self.crossy=crossy
        self.saveoutput = saveoutput #Do you want to save all data outputs?
        self.headless = headless #Are you running a monitor and want to visual the simulation? Note, this adds significant calculation time
        self.maxtime = maxtime #How many seconds in simulation do you want to simulate?
        self.timestep = timestep #Timestep size in simulation, seconds
        self.motor_system = sim.System("m1") #Create the system


        self.s1 = time.perf_counter()
        self.mtorque = [0,0] #set intial torque   
        self.maxtorque=abs(maxtorque)
        self.arm1 = sim.Motor_arm(self.motor_system.system,False,self.material,self.crossx,self.crossy,(0,0,0),(0,0,self.length1),0.000,10) #create arm in simulation
        self.arm2 = sim.Motor_arm(self.motor_system.system,False,self.material,self.crossx,self.crossy,(0,0,self.length1),(0,0,self.length1+self.length2),0.000,10,origin=False,stator_constraint=self.arm1.arm_tip)#create attached second arm
        
        self.getstate() 
        self.state = self.state_new
        self.target = np.array(target)
        self.position_original = np.array([self.state[6],self.state[7]])
        self.step = 0
        if not headless:
            self.motor_system.Window(self.arm1,self.arm2,timestep,headless=headless,print_time=True) #create a window to view system if not headless

    def forwardStep(self, action):#action is a 1x2 list:
        self.step = self.step+1
        #Determine current position (for reward calculations):
        self.state = self.state_new

        #determine torque values to apply:
        for i in range(0,len(action)):
            if action[i] == 0:
                self.mtorque[i] = 0
            if abs(self.mtorque[i])<self.maxtorque:
                if action[i] >0:
                    self.mtorque[i] = self.mtorque[i]+self.maxtorque/5 #ramp forces over 5 "steps"
                if action[i]<0:
                    self.mtorque[i] = self.mtorque[i]-self.maxtorque/5 #ramp forces over 5 "steps"

            if abs(self.mtorque[i]) == self.maxtorque:
                if ((action[i]>0) and (self.mtorque[i]<0)):
                    self.mtorque[i] = self.mtorque[i]+self.maxtorque/5 
                if ((action[i]<0) and (self.mtorque[i]>0)):
                    self.mtorque[i] = self.mtorque[i]-self.maxtorque/5 
        self.arm1.set_torque(float(self.mtorque[0]))
        self.arm2.set_torque(float(self.mtorque[1]))
        self.motor_system.do_sim_step(self.timestep)
        

        #Determine new state:
        self.getstate()

        return(self.state,self.state_new,action)
                



    
    def render(self, mode = 'human',close = False):
        if self.headless == False:
            self.motor_system.window.BeginScene() 
            self.motor_system.window.DrawAll()
            self.motor_system.window.EndScene()
        else:
            print("Don't forget to set headless to False")
        
    def reward(self):
        tip_previous = np.array([self.state[6],self.state[7]])
        tip_new = np.array([self.state_new[6],self.state_new[7]])

        dist_previous = (tip_previous-self.target)
        dist_previous = np.sqrt(dist_previous[0]**2+dist_previous[1]**2)
        dist_new = (tip_new-self.target)
        dist_new = np.sqrt(dist_new[0]**2+dist_new[1]**2)
        dist_change = dist_previous-dist_new
        dist_max = self.target-self.position_original
        dist_max = np.sqrt(dist_max[0]**2+dist_max[1]**2)
        if dist_change > 0:
            reward = dist_change/dist_max
        elif dist_change <0:
            reward = 2*dist_change/dist_max
        else:
            reward = 0
        return(reward)
    def save(self): #Future function to save all pyChrono data to create deep network which simulates the motion.
        pass



if __name__=="__main__":
    steel = Multi_armMaterial("steel",3.0E9,0.5,1300)
    environmentTest = Multi_armEnv()
    environmentTest.reset(False,True,3,0.02,0.0125,1.5,1,steel,0.001,1,[-0.5,1.25])
    state_tensor = []

    for i in range(3000):
        #environmentTest.render()
        state,state_new,action = environmentTest.forwardStep([1,1])
        reward = environmentTest.reward()
        state_tensor.append((state,state_new,action,reward))

    aa = time.perf_counter()-environmentTest.s1
    environmentTest.reset(False,True,3,0.02,0.0125,1.5,1,steel,0.001,1,[-0.5,1.25])
    for i in range(3000):
        #environmentTest.render()
        environmentTest.forwardStep([1,1])
        environmentTest.reward()
    ab = time.perf_counter()-environmentTest.s1
    environmentTest.reset(False,True,3,0.02,0.0125,1.5,1,steel,0.001,1,[-0.5,1.25])
    for i in range(3000):
        #environmentTest.render()
        environmentTest.forwardStep([1,1])
        environmentTest.reward()

    ac = time.perf_counter()-environmentTest.s1
    environmentTest.reset(False,True,3,0.02,0.0125,1.5,1,steel,0.001,1,[-0.5,1.25])
    for i in range(3000):
        #environmentTest.render()
        environmentTest.forwardStep([1,1])
        environmentTest.reward()

    ad = time.perf_counter()-environmentTest.s1
    print(aa,ab,ac,ad)


