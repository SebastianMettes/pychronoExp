import pychrono as chrono
import pychrono.fea as fea
#import pychrono.mkl as mkl
try: 
    import pychrono.irrlicht as chronoirr
except:
    print("Only Headless mode is supported")
    pass
import time
import random

chrono.SetChronoDataPath('/~/pychrono-5.0.0-py37_9/share/chrono/data/') 


class Material():
    def __init__(self,name, modulus, poisson, density):
        self.name = name
        self.modulus = modulus
        self.poisson = poisson
        self.density = density
        self.shear = self.poisson*self.modulus



class System():
    def __init__(self,name):
        self.system = chrono.ChSystemNSC()
        self.name = name
        solver = chrono.ChSolverSparseLU()
        self.system.SetSolver(solver)

    
    def Window(self,arm1,arm2,timestep,print_time = False,headless=True,):

        if not headless:
            self.window =chronoirr.ChIrrApp(self.system,self.name,chronoirr.dimension2du(1920,1080)) #Create window for visualization
            self.window.AddTypicalCamera(chronoirr.vector3df(1,1,2))
            self.window.AddTypicalLights()
            self.window.AddTypicalSky()
            self.window.AssetBindAll()
            self.window.AssetUpdateAll()        
            self.window.SetTimestep(timestep)
            self.window.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))


    def do_sim_step(self,timestep):
        self.system.DoStepDynamics(timestep)

class Motor_arm():
    def __init__(self,sys,gravity,material,width,height,position_base,position_tip,damping,elements,torque=10,origin=True,stator_constraint = None):
        self.material = material
        self.mesh = fea.ChMesh()
        self.mesh.SetAutomaticGravity(gravity)

        self.section = fea.ChBeamSectionEulerAdvanced()
        self.section.SetAsRectangularSection(width,height)
        self.section.SetYoungModulus(material.modulus)
        self.section.SetGshearModulus(material.shear)
        self.section.SetDensity(material.density)
        self.section.SetBeamRaleyghDamping(damping)
        
        self.position_base = chrono.ChVectorD(*position_base)
        self.position_tip = chrono.ChVectorD(*position_tip)

        self.builder = fea.ChBuilderBeamEuler() #Use the beam builder assembly method to assembly each beam
        self.builder.BuildBeam(self.mesh,self.section,elements,self.position_base,self.position_tip,chrono.ChVectorD(0,1,0),)
        import numpy as np
 


        self.stator = chrono.ChBodyEasyCylinder(0.01,0.01,1000)
        self.stator.SetPos(self.position_base)
        self.stator.SetBodyFixed(origin)
        self.frame = chrono.ChFrameD(self.stator)
        sys.Add(self.stator) 
        if (origin == False) and (stator_constraint is not None): #If the beam is not located at the origin, it must need to be constrained to another beam 
            self.constraint = chrono.ChLinkMateGeneric()
            self.constraint.Initialize(self.stator,stator_constraint,False,chrono.ChFrameD(self.stator),chrono.ChFrameD(stator_constraint))
            self.constraint.SetConstrainedCoords(True,True,True,True,True,True)
            sys.Add(self.constraint)
            self.frame = chrono.ChFrameD(self.stator)
        self.rotor = chrono.ChBodyEasyCylinder(0.011,0.011,1000)
        self.rotor.SetPos(self.position_base)
        sys.Add(self.rotor)

        
        self.frame.SetRot(chrono.Q_from_AngAxis(chrono.CH_C_PI_2, chrono.VECT_X))#Rotate the direction of rotation to be planar (x-z plane)


        self.motor = chrono.ChLinkMotorRotationTorque()
        self.motor.Initialize(self.rotor,self.stator,self.frame)
        sys.Add(self.motor)
        self.motor.SetTorqueFunction(chrono.ChFunction_Const(torque))
        
        self.arm_base = (self.builder.GetLastBeamNodes().front())
        self.arm_tip = (self.builder.GetLastBeamNodes().back())

        self.mate = chrono.ChLinkMateGeneric()
        self.mate.Initialize(self.builder.GetLastBeamNodes().front(),self.rotor,chrono.ChFrameD(self.builder.GetLastBeamNodes().front().GetPos()))#constrain beam to rotor
        self.mate.SetConstrainedCoords(True,True,True,True,True,True) #constraints must be in format: (True,True,True,True,True,True) to constrain x,y,z,rotx,roty,rotz coordinates
        sys.Add(self.mate)

        self.visual = fea.ChVisualizationFEAmesh(self.mesh)
        self.visual.SetFEMdataType(fea.ChVisualizationFEAmesh.E_PLOT_ELEM_BEAM_MZ)
        self.visual.SetColorscaleMinMax(-1.4,1.4)
        self.visual.SetSmoothFaces(True)
        self.visual.SetWireframe(False)
        self.mesh.AddAsset(self.visual)

        sys.Add(self.mesh)
    def set_torque(self,torque):
        self.motor.SetTorqueFunction(chrono.ChFunction_Const(torque))




