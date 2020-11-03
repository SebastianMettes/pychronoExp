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

testrun = "0.005"
#create the simulation
#note everything is in meters, kg, metric units
savefile1 = []
savefile2 = []
headless = True
maxtime=5
timestep = 0.005

motor_system = sim.System("test")
arm1 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,0),(0,0,1),0.000,10) #create arm in simulation
arm2 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,1),(0,0,1.5),0.000,10,origin=False,stator_constraint=arm1.arm_tip)#create attached second arm

if not headless:
    motor_system.window(arm1,arm2,timestep,headless=headless,print_time=True) #create window to view system

s1 = time.perf_counter()
while(motor_system.system.GetChTime()<maxtime):
    if not headless:
        motor_system.window.BeginScene()
        motor_system.window.DrawAll()
        m1t = 1
        m2t = -1
        #m1t = random.randrange(-10,11,1)*1.5
        #m2t = random.randrange(-10,11,1)*0.25
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        motor_system.window.EndScene()
        #print(arm1.arm_tip.GetPos())
        print(motor_system.system.GetChTime())
        arm2Pos = arm2.arm_tip.GetPos()
        arm1Pos = arm1.arm_tip.GetPos()
        #import pdb; pdb.set_trace()
        arm2PosList = [arm2Pos.x,arm2Pos.z]
        arm1PosList = [arm1Pos.x,arm1Pos.z]        
        savefile2.append(arm2PosList)
        savefile1.append(arm1PosList)
        #print(time.perf_counter()-s1)
    else:

        m1t = 1
        m2t = -1
        #m1t = random.randrange(-10,11,1)*1.5
        #m2t = random.randrange(-10,11,1)*0.25
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        #print(arm1.arm_tip.GetPos())   
        print(motor_system.system.GetChTime())     
        #print(time.perf_counter()-s1)
        arm2Pos = arm2.arm_tip.GetPos()
        arm1Pos = arm1.arm_tip.GetPos()
        #import pdb; pdb.set_trace()
        arm2PosList = [arm2Pos.x,arm2Pos.z]
        arm1PosList = [arm1Pos.x,arm1Pos.z]        
        savefile2.append(arm2PosList)
        savefile1.append(arm1PosList)

np.save(testrun+"filetip2.txt",np.array(savefile2))
np.save(testrun+'filetip1.txt',np.array(savefile1))
#print(arm2.arm_tip.GetPos())
#print(motor_system.system.GetChTime()) 
print(time.perf_counter()-s1)

