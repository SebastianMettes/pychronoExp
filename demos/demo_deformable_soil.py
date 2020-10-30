# =============================================================================
# PROJECT CHRONO - http://projectchrono.org
#
# Copyright (c) 2014 projectchrono.org
# All rights reserved.
#
# Use of this source code is governed by a BSD-style license that can be found
# in the LICENSE file at the top level of the distribution and at
# http://projectchrono.org/license-chrono.txt.
#
# =============================================================================
# Authors: Radu Serban
# =============================================================================
# Demo of the SCM semi-empirical model for deformable soil
# =============================================================================

import pychrono.core as chrono
import pychrono.irrlicht as chronoirr
import pychrono.vehicle as veh

import math

# The path to the Chrono data directory containing various assets (meshes, textures, data files)
# is automatically set, relative to the default location of this demo.
# If running from a different directory, you must change the path to the data directory with: 
#chrono.SetChronoDataPath('path/to/data')

# Global parameters for tire
tire_rad = 0.8
tire_vel_z0 = -3
tire_center = chrono.ChVectorD(0, 0.02 + tire_rad, 0)
tire_w0 = tire_vel_z0 / tire_rad

# ----------------------------
# Create the mechanical system
# ----------------------------

mysystem = chrono.ChSystemSMC()

# Create the ground
ground = chrono.ChBody()
ground.SetBodyFixed(True)
mysystem.Add(ground)

# Create the rigid body with contact mesh
body = chrono.ChBody()
mysystem.Add(body)
body.SetMass(500)
body.SetInertiaXX(chrono.ChVectorD(20, 20, 20))
body.SetPos(tire_center + chrono.ChVectorD(0, 0.3, 0))

# Load mesh
mesh = chrono.ChTriangleMeshConnected()
mesh.LoadWavefrontMesh(chrono.GetChronoDataFile('tractor_wheel.obj'))

# Set visualization assets
vis_shape = chrono.ChTriangleMeshShape()
vis_shape.SetMesh(mesh)
body.AddAsset(vis_shape)
body.AddAsset(chrono.ChColorAsset(0.3, 0.3, 0.3))

# Set collision shape
body.GetCollisionModel().ClearModel()
body.GetCollisionModel().AddTriangleMesh(mesh,                    # the mesh 
                                         False,                   # is it static?
                                         False,                   # is it convex?
                                         chrono.ChVectorD(0,0,0), # position on body
                                         chrono.ChMatrix33D(1),   # orientation on body 
                                         0.01)                    # "thickness" for increased robustness
body.GetCollisionModel().BuildModel()
body.SetCollide(True)

# Create motor
motor = chrono.ChLinkMotorRotationAngle()
motor.SetSpindleConstraint(chrono.ChLinkMotorRotation.SpindleConstraint_OLDHAM)
motor.SetAngleFunction(chrono.ChFunction_Ramp(0, math.pi / 4))
motor.Initialize(body, ground, chrono.ChFrameD(tire_center, chrono.Q_from_AngY(math.pi/2)))
mysystem.Add(motor)

# ------------------------
# Create SCM terrain patch
# ------------------------

# Note that SCMDeformableTerrain uses a default ISO reference frame (Z up). Since the mechanism is modeled here in
# a Y-up global frame, we rotate the terrain plane by -90 degrees about the X axis.
terrain = veh.SCMDeformableTerrain(mysystem)
terrain.SetPlane(chrono.ChCoordsysD(chrono.ChVectorD(0,0,0.5), chrono.Q_from_AngX(-math.pi/2)))
terrain.Initialize(0.2, 1.5, 5, 20, 60)

# Set soil properties
terrain.SetSoilParameters(0.2e6,  # Bekker Kphi
                          0,      # Bekker Kc
                          1.1,    # Bekker n exponent
                          0,      # Mohr cohesive limit (Pa)
                          30,     # Mohr friction limit (degrees)
                          0.01,   # Janosi shear coefficient (m)
                          4e7,    # Elastic stiffness (Pa/m), before plastic yield, must be > Kphi
                          3e4)    # Damping (Pa s/m), proportional to negative vertical speed (optional)

# Enable bulldozing effects (inflate soil at the border of the rut)
terrain.SetBulldozingFlow(True)
terrain.SetBulldozingParameters(55,   # angle of friction for erosion of displaced material at the rut border
                                1,    # displaced material vs downward pressed material.
                                5,    # number of erosion refinements per timestep
                                10)   # number of concentric vertex selections subject to erosion

# Turn on the automatic mesh refinement
terrain.SetAutomaticRefinement(True)
terrain.SetAutomaticRefinementResolution(0.04)

# Set terrain visualization mode
terrain.SetPlotType(veh.SCMDeformableTerrain.PLOT_PRESSURE, 0, 30000.2)

# ------------------------------------------
# Create the Irrlicht run-time visualization
# ------------------------------------------

myapplication = chronoirr.ChIrrApp(mysystem, 'Deformable soil', chronoirr.dimension2du(1280,720), False, True)
myapplication.AddTypicalSky()
myapplication.AddTypicalLogo(chrono.GetChronoDataFile('logo_pychrono_alpha.png'))
myapplication.AddTypicalCamera(chronoirr.vector3df(1.0,1.4,-1.2), chronoirr.vector3df(0,tire_rad,0))
myapplication.AddTypicalLights()
myapplication.AddLightWithShadow(chronoirr.vector3df(1.5,5.5,-2.5),    # point
                                 chronoirr.vector3df(0,0,0),           # aim point
                                 3,                                    # radius (power)
                                 2.2, 7.2,                             # near, far
                                 40,                                   # angle of FOV
                                 512,                                  # resoluition
                                 chronoirr.SColorf(0.8,0.8,1))         # light color
myapplication.AssetBindAll();
myapplication.AssetUpdateAll();
myapplication.AddShadowAll();

# ------------------
# Run the simulation
# ------------------

myapplication.SetTimestep(0.002)

while(myapplication.GetDevice().run()):
    myapplication.BeginScene()
    myapplication.DrawAll()
    myapplication.DoStep()
    myapplication.EndScene()
