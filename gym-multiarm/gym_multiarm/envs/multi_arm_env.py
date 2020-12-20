import gym
import pychrono as chrono
import pychrono.fea as fea
import pychrono.mkl as mkl
import pychrono.irrlicht as chronoirr
import time
import random
import numpy as np
from packages import multi_arm_assembler_3
from gym import error, spaces, utils
from gym.utils import seeding


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
        pass
    def step(self, action):
        pass
    def reset(self):
        pass
    def render(self, mode = 'human',close = False):
        pass
