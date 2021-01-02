import multi_arm_assembler_3 as sim
import time
import random
import numpy as np
#Setup the materials
def steel():
    return sim.Material("steel",190E9,0.25,1000)#Create a material
def pla():
    return sim.Material("pla",3E9,0.3,1000)
def abs():
    return sim.Material("abs",0.35,1000)


#note everything is in meters, kg, N, metric units

#Stuff you should modify:
saveoutput = False
headless = False #Are you running a monitor and want to visual the simulation? Note, this adds significant calculation time
ramped = False
maxtime=3 #How many seconds in simulation do you want to simulate?
timestep = 0.05 #Timestep size in simulation, seconds
motor_system = sim.System("test") #Create the system
arm1 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,0),(0,0,1),0.000,10) #create arm in simulation
arm2 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,1),(0,0,1.5),0.000,10,origin=False,stator_constraint=arm1.arm_tip)#create attached second arm

#The rest of the code...
stepname = str(timestep)
savefile1 = [] #empty list to append position data to (arm 1)
savefile2 = [] #empty list to append position data to (arm 2)
if not headless:
    motor_system.window(arm1,arm2,timestep,headless=headless,print_time=True) #create window to view system if not headless

s1 = time.perf_counter() #track how long simulation takes to run
step = 0 #step counter
m1t = 0
m2t = 0 #initial setting prior to ramping
while(motor_system.system.GetChTime()<maxtime):
    if not headless:
        if ramped == True:  
            if m1t < 0.5:
                m1t = m1t+timestep
            if m2t >-0.5:
                m2t = m2t-timestep
        else:
            m1t = 1
            m2t = -1
        motor_system.window.BeginScene() 
        motor_system.window.DrawAll()
        m1t = 1 #set torque to motor
        m2t = -1 #set torque to motor
        #m1t = random.randrange(-10,11,1)*1.5 #set random torque to motor at every step
        #m2t = random.randrange(-10,11,1)*0.25 #set random torque to motor at every step
        arm1.set_torque(float(m1t)) #Apply torque
        arm2.set_torque(float(m2t)) #Apply torque
        motor_system.do_sim_step(timestep)    
        motor_system.window.EndScene()
        #print(arm1.arm_tip.GetPos())
        #print(motor_system.system.GetChTime())
        if saveoutput == True:
            arm2Pos = arm2.arm_tip.GetPos() #Pull position data
            arm1Pos = arm1.arm_tip.GetPos()
            #import pdb; pdb.set_trace()
            arm2PosList = [arm2Pos.x,arm2Pos.z] #Put into correct format
            arm1PosList = [arm1Pos.x,arm1Pos.z]        
            savefile2.append(arm2PosList) #Append to textfile
            savefile1.append(arm1PosList)
            np.savetxt(stepname+arm2.material.name+"0.5N-tip2position.txt",np.array(savefile2))
            #print(time.perf_counter()-s1)
    else: #if headless

    #is ramped?
    #   
        if ramped == True:  
            if m1t < 0.5:
                m1t = m1t+timestep
            if m2t >-0.5:
                m2t = m2t-timestep
        else:
            m1t = 1
            m2t = -1
        #m1t = random.randrange(-10,11,1)*1.5
        #m2t = random.randrange(-10,11,1)*0.25
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        #print(arm1.arm_tip.GetPos())   
        #print(motor_system.system.GetChTime())     
        #print(time.perf_counter()-s1)
        if saveoutput == True:
            arm2Pos = arm2.arm_tip.GetPos()
            arm1Pos = arm1.arm_tip.GetPos()
            #import pdb; pdb.set_trace()
            arm2PosList = [arm2Pos.x,arm2Pos.z]
            arm1PosList = [arm1Pos.x,arm1Pos.z]        
            savefile2.append(arm2PosList)
            savefile1.append(arm1PosList)
            np.savetxt(stepname+arm2.material.name+"0.5N-tip2position.txt",np.array(savefile2))


#np.savetxt("steel"+testrun+'filetip1.txt',np.array(savefile1))
#print(arm2.arm_tip.GetPos())
#print(motor_system.system.GetChTime()) 
print(time.perf_counter()-s1)

