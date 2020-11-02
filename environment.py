import multi_arm_assembler_3 as sim
import time
import random
#Setup the materials
def steel():
    return sim.Material("steel",190E9,0.25,1000)#Create a material
def pla():
    return sim.Material("pla",3E9,0.3,1000)
def abs():
    return sim.Material("abs",0.35,1000)

#create the simulation
#note everything is in meters, kg, metric units

headless = False
maxtime=4
timestep = 0.005

motor_system = sim.System("test")
arm1 = sim.Motor_arm(motor_system.system,False,steel(),0.025,0.0125,(0,0,0),(0,0,1),0.0005,10) #create arm in simulation
arm2 = sim.Motor_arm(motor_system.system,False,steel(),0.025,0.0125,(0,0,1),(0,0,1.5),0.0005,10,origin=False,stator_constraint=arm1.arm_tip)#create attached second arm

if not headless:
    motor_system.window(arm1,arm2,timestep,headless=headless,print_time=True) #create window to view system

s1 = time.perf_counter()
while(motor_system.system.GetChTime()<maxtime):
    if not headless:
        motor_system.window.BeginScene()
        motor_system.window.DrawAll()
        m1t = random.randrange(-10,11,1)*1.5
        m2t = random.randrange(-10,11,1)*0.25
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        motor_system.window.EndScene()
        print(arm1.arm_tip.GetPos())
        print(motor_system.system.GetChTime())
        print(time.perf_counter()-s1)
    else:

        m1t = random.randrange(-10,11,1)*1.5
        m2t = random.randrange(-10,11,1)*0.25
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        #motor_system.window.EndScene()
        print(arm1.arm_tip.GetPos())   
        print(motor_system.system.GetChTime())     
        print(time.perf_counter()-s1)