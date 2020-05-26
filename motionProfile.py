import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve

pi = np.pi
cos = np.cos

class FoilGeo(object):
    """Foil geometry conditions are used to explore different sizes and shapes"""
    #class body definition
    
    def __init__(self, chord=0.15, leading_ellipse_y = 0.00325, leading_ellipse_xyRatio = 6, trailing_ellipse_y = 0.002, trailing_ellipse_xyRatio = 6):
        self.leading_ellipse_y = leading_ellipse_y
        self.leading_ellipse_x = leading_ellipse_y*leading_ellipse_xyRatio
        self.leading_ellipse_origin = -chord/2 + self.leading_ellipse_x
        self.trailing_ellipse_y = trailing_ellipse_y
        self.trailing_ellipse_x = trailing_ellipse_y*trailing_ellipse_xyRatio
        self.trailing_ellipse_origin = chord/2 - self.trailing_ellipse_x
        self.chord = chord
        
    def gen_foilshape(self):
        #Solve for tangent lines to the leading and trailing edge ellipses
        m, k = symbols('m k')
        eq1 = Eq((self.leading_ellipse_x**2*k*m - self.leading_ellipse_origin*self.leading_ellipse_y**2)**2 - (self.leading_ellipse_y**2+self.leading_ellipse_x**2*m**2)*(self.leading_ellipse_origin**2*self.leading_ellipse_y**2+self.leading_ellipse_x**2*k**2-self.leading_ellipse_y**2*self.leading_ellipse_x**2),0)
        eq2 = Eq((self.trailing_ellipse_x**2*k*m - self.trailing_ellipse_origin*self.trailing_ellipse_y**2)**2 - (self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*m**2)*(self.trailing_ellipse_origin**2*self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*k**2-self.trailing_ellipse_y**2*self.trailing_ellipse_x**2),0)
        sol_dict = solve((eq1,eq2),(m,k))
        
        # Solve for the intersection point at the leading edge ellipse
        x, y = symbols('x y')
        eqT = Eq(sol_dict[1][0]*x+sol_dict[1][1]-y,0)
        eqE = Eq((x-self.leading_ellipse_origin)**2/self.leading_ellipse_x**2 + y**2/self.leading_ellipse_y**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.leading_ellipse_xT = abs(sol_xy[0][0])
        self.leading_ellipse_yT = abs(sol_xy[0][1])
        
        # Solve for the intersection point at the trailing edge ellipse
        eqE = Eq((x-self.trailing_ellipse_origin)**2/self.trailing_ellipse_x**2 + y**2/self.trailing_ellipse_y**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.trailing_ellipse_xT = abs(sol_xy[0][0])
        self.trailing_ellipse_yT = abs(sol_xy[0][1])
        
    def update_leading_ellipse_y(self, leading_ellipse_y):
        self.leading_ellipse_y = leading_ellipse_y
    
    def update_leading_ellipse_xyRatio(self, leading_ellipse_xyRatio):
        self.leading_ellipse_x = leading_ellipse_xyRatio*self.leading_ellipse_y

    def update_trailing_ellipse_y(self, trailing_ellipse_y):
        self.trailing_ellipse_y = trailing_ellipse_y
    
    def update_trailing_ellipse_xyRatio(self, trailing_ellipse_xyRatio):
        self.leading_ellipse_x = trailing_ellipse_xyRatio*self.leading_ellipse_y
        
    def update_chord(self, chord):
        self.chord = chord
    

class FoilProf(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, f, theta, steps_per_cycle, total_cycles=2, density=1.225, hc=0.5, chord=0.15):
        self.freq = f                       #frequency of heaving motion [Hz]
        self.theta0 = np.radians(theta)             #pitching amplitude [deg]
        self.dt = 1/(f*steps_per_cycle)
        self.T = round(total_cycles/f,6)
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
    print(check.leading_ellipse_xT)
    print(check.trailing_ellipse_xT)
    print(check.leading_ellipse_yT)
    print(check.trailing_ellipse_yT)

def mod_geoScript(foil):
    """Takes the foil geometry and create script for importing to Ansys"""
    
