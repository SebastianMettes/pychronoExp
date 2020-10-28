import multi_arm_assembler_3 as sim


#Setup the materials
def steel():
    return sim.Material("steel",190E9,0.25,8000)#Create a material
def pla():
    return sim.Material("pla",3E9,0.3,1000)
def abs():
    return sim.Material("abs",0.35,1000)

#create the simulation

motor_system = sim.System("test")


arm1 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,0),(0,0,1),0.0005,10) #create arm in simulation
arm2 = sim.Motor_arm(motor_system.system,False,pla(),0.025,0.0125,(0,0,1),(0,0,1.5),0.0005,10,origin=False,stator_constraint=arm1.arm_tip)#create attached second arm

headless = False
maxtime=0.2
timestep = 0.005

if not headless:
    motor_system.window(arm1,arm2,timestep,headless=headless,print_time=True) #create window to view system

while(motor_system.system.GetChTime()<maxtime):
    if not headless:
        motor_system.window.BeginScene()
        motor_system.window.DrawAll()
        m1t = input("enter arm1 torque: ")
        m2t = input("enter arm2 torque: ")
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        motor_system.window.EndScene()
        print(arm1.arm_tip.GetPos())
        print(motor_system.system.GetChTime())
    else:
        #motor_system.window.BeginScene()
        #motor_system.window.DrawAll()
        m1t = input("enter arm1 torque: ")
        m2t = input("enter arm2 torque: ")
        arm1.set_torque(float(m1t))
        arm2.set_torque(float(m2t))
        motor_system.do_sim_step(timestep)    
        #motor_system.window.EndScene()
        print(arm1.arm_tip.GetPos())   
        print(motor_system.system.GetChTime())     