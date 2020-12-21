import gym
import pychrono as chrono
import pychrono.fea as fea
import pychrono.mkl as mkl
import pychrono.irrlicht as chronoirr
import time
import random
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding
from packages import multi_arm_assembler_3

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

    def setup(self,saveoutput,headless,maxtime,crossx,crossy,length1,length2,material,timestep,maxtorque,target):
        #Check input information:
        if len(target) != 2:
            print("Target is list of length 2, [x,y] coordinates")
            quit()

        self.saveoutput = saveoutput #Do you want to save all data outputs?
        if self.saveoputput == True:
            self.stepname = str(timestep)
            self.savefile1 = []
        self.headless = headless #Are you running a monitor and want to visual the simulation? Note, this adds significant calculation time
        self.maxtime = maxtime #How many seconds in simulation do you want to simulate?
        self.timestep = timestep #Timestep size in simulation, seconds
        self.motor_system = sim.System("test") #Create the system
        self.arm1 = sim.Motor_arm(motor_system.system,False,material,crossx,crossy,(0,0,0),(0,0,length1),0.000,10) #create arm in simulation
        self.arm2 = sim.Motor_arm(motor_system.system,False,material,crossx,crossy,(0,0,length1),(0,0,length1+length2),0.000,10,origin=False,stator_constraint=arm1.arm_tip)#create attached second arm
        if not headless:
            self.motor_system.window(arm1,arm2,timestep,headless=headless,print_time=True) #create a window to view system if not headless
        self.s1 = time.perf_counter()
        self.step = 0
        self.mtorque = [0,0] #set intial torque   
        self.maxtorque=abs(maxtorque)
        self.target = target   
        arm1Pos = arm1.arm_tip.GetPos()
        arm2Pos = arm2.arm_tip.GetPos()
        arm1Vel = arm1.arm_tip.GetVel()
        arm2Vel = arm2.arm_tip.GetVel()
        arm1Acc = arm1.arm_tip.GetAcc()
        arm2Acc = arm2.arm_tip.GetAcc()
        

        self.state = []#ADD INFORMATION, Link 1 X,Y, Vx, Vy, Ax, Ay, Link 2 X,Y,Vx,Vy,Ax,Ay, Torque 1, Torque 2, Theta1,Theta2, AngVel1,AngVel2,TargetX,TargetY
    def step(self, action):#action is a 1x2 list:
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
        self.state_new = []#NEED TO FILL OUT
                

    def reset(self):
        pass
    def render(self, mode = 'human',close = False):
        pass
    def reward(self):
        pass
    def save(self):
        pass
