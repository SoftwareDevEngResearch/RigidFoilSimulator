import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve

pi = np.pi
cos = np.cos

class FoilGeo(object):
    """Foil geometry conditions are used to explore different sizes and shapes"""
    #class body definition
    
    def __init__(self, chord=0.15, LEy = 0.00325, LEAR = 6, TEy = 0.002, TEAR = 6):
        self.LEy = LEy
        self.LEx = LEy*LEAR
        self.LEc = -chord/2 + self.LEx
        self.TEy = TEy
        self.TEx = TEy*TEAR
        self.TEc = chord/2 - self.TEx
        self.chord = chord
        
    def gen_foilshape(self):
        #Solve for tangent lines to the leading and trailing edge ellipses
        m, k = symbols('m k')
        eq1 = Eq((self.LEx**2*k*m - self.LEc*self.LEy**2)**2 - (self.LEy**2+self.LEx**2*m**2)*(self.LEc**2*self.LEy**2+self.LEx**2*k**2-self.LEy**2*self.LEx**2),0)
        eq2 = Eq((self.TEx**2*k*m - self.TEc*self.TEy**2)**2 - (self.TEy**2+self.TEx**2*m**2)*(self.TEc**2*self.TEy**2+self.TEx**2*k**2-self.TEy**2*self.TEx**2),0)
        sol_dict = solve((eq1,eq2),(m,k))
        
        # Solve for the intersection point at the leading edge ellipse
        x, y = symbols('x y')
        eqT = Eq(sol_dict[1][0]*x+sol_dict[1][1]-y,0)
        eqE = Eq((x-self.LEc)**2/self.LEx**2 + y**2/self.LEy**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.LExT = abs(sol_xy[0][0])
        self.LEyT = abs(sol_xy[0][1])
        
        # Solve for the intersection point at the trailing edge ellipse
        eqE = Eq((x-self.TEc)**2/self.TEx**2 + y**2/self.TEy**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.TExT = abs(sol_xy[0][0])
        self.TEyT = abs(sol_xy[0][1])
        
    def update_LEy(self, LEy):
        self.LEy = LEy
    
    def update_LEAR(self, LEAR):
        self.LEx = LEAR*self.LEy

    def update_TEy(self, TEy):
        self.TEy = TEy
    
    def update_TEAR(self, TEAR):
        self.LEx = TEAR*self.LEy
        
    def update_chord(self, chord):
        self.chord = chord
    

class FoilProf(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, f, theta, dtdT, cyc=2, density=1.225, hc=0.5, chord=0.15):
        self.freq = f                       #frequency of heaving motion [Hz]
        self.theta0 = np.radians(theta)             #pitching amplitude [deg]
        self.dt = 1/(f*dtdT)
        self.T = round(cyc/f,4)
        self.rho = density
        self.chord = chord
        self.h0 = hc*self.chord
        samp = int(np.ceil(self.T/self.dt) + 1)
        self.time = [0]*samp
        self.h = [0]*samp
        self.theta = [0]*samp
        for x in range(samp):
            ti = round(x*self.dt,5)
            self.time[x] = ti
            self.h[x] = 2*pi*f*self.h0*cos(2*pi*f*ti+pi/2)
            self.theta[x] = 2*pi*f*self.theta0*cos(2*pi*f*ti)
    def update_h0(self,hc):
        self.h0 = hc*self.chord
        samp = int(np.ceil(self.T/self.dt) + 1)
        self.h = [0]*samp
        for x in range(samp):
            ti = round(x*self.dt,5)
            self.h[x] = 2*pi*self.f*self.h0*cos(2*pi*self.f*ti+pi/2)
        print("New heaving amplitude = ", self.h0)
    update_h0(self,0.3)

if __name__ == "__main__":
    """testing script functionality"""

    k008 = FoilProf(1.6,70,1000)
    plt.plot(k008.time, k008.h, label = "heaving velocity")
    plt.plot(k008.time, k008.theta, label = "pitching velocity")
    plt.xlabel('time [s]')
    plt.legend()
    # plt.show()
    # test = k008.update_h0(0.3)

    check = FoilGeo()
    check.gen_foilshape()
    print(check.LExT)
    print(check.TExT)
    print(check.LEyT)
    print(check.TEyT)

def mod_geoScript(foil):
    """Takes the foil geometry and create script for importing to Ansys"""
    
