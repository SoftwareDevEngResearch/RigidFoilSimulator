import numpy as np
import math
import matplotlib as plt

pi = math.pi

class FoilParam(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, f, theta, dt, t, density=1.225, hc=0.5):
        self.freq = f                       #frequency of heaving motion [Hz]
        self.theta0 = theta*10              #pitching amplitude [deg]
        self.dt = dt
        self.t = t
        self.rho = density
        self.chord = 0.15
        self.hc = hc
        self.h0 = self.hc*self.chord
        samp = math.ceil(t/dt) + 1
        self.time = [0]*samp
        self.h = [0]*samp
        for x in range(samp):
            self.time[x] = round(x*dt,5)
            self.h[x] = 2*pi*f*self.h0*math.cos(2*pi*f*self.time[x]+pi/2)
            

k008 = FoilParam(1.6,70,0.1,4)
