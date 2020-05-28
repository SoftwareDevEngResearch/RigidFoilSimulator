import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve

pi = np.pi
cos = np.cos

class FoilGeo(object):
    """Foil geometry conditions are used to explore different sizes and shapes"""
    #class body definition
    
    def __init__(self, chord=0.15, leading_ellipse_y = 0.0065/2, leading_ellipse_x = 0.0065*3, trailing_ellipse_y = 0.0065/2, trailing_ellipse_x=0.0065*3):
        """Initializes the main parameters for DesignModeler, default parameters are for the flat rigid plate geometry"""
        self.leading_ellipse_y = leading_ellipse_y
        self.leading_ellipse_x = leading_ellipse_x
        self.leading_ellipse_origin = -chord/2 + self.leading_ellipse_x
        self.trailing_ellipse_y = trailing_ellipse_y
        self.trailing_ellipse_x = trailing_ellipse_x
        self.trailing_ellipse_origin = chord/2 - self.trailing_ellipse_x
        self.chord = chord
        
        #Solve for tangent lines to the leading and trailing edge ellipses
        m, k = symbols('m k')
        eq1 = Eq((self.leading_ellipse_x**2*k*m - self.leading_ellipse_origin*self.leading_ellipse_y**2)**2 - (self.leading_ellipse_y**2+self.leading_ellipse_x**2*m**2)*(self.leading_ellipse_origin**2*self.leading_ellipse_y**2+self.leading_ellipse_x**2*k**2-self.leading_ellipse_y**2*self.leading_ellipse_x**2),0)
        eq2 = Eq((self.trailing_ellipse_x**2*k*m - self.trailing_ellipse_origin*self.trailing_ellipse_y**2)**2 - (self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*m**2)*(self.trailing_ellipse_origin**2*self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*k**2-self.trailing_ellipse_y**2*self.trailing_ellipse_x**2),0)
        sol_dict = solve((eq1,eq2),(m,k))
        
        # Define the equation for tangent lines
        x, y = symbols('x y')
        eqT = Eq(sol_dict[1][0]*x+sol_dict[1][1]-y,0)
        
        # Solve for the intersection point at the leading edge ellipse
        eqE = Eq((x-self.leading_ellipse_origin)**2/self.leading_ellipse_x**2 + y**2/self.leading_ellipse_y**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.leading_ellipse_xT = abs(sol_xy[0][0])
        self.leading_ellipse_yT = abs(sol_xy[0][1])
        
        # Solve for the intersection point at the trailing edge ellipse
        eqE = Eq((x-self.trailing_ellipse_origin)**2/self.trailing_ellipse_x**2 + y**2/self.trailing_ellipse_y**2 - 1,0)
        sol_xy = solve((eqT,eqE),(x,y))
        self.trailing_ellipse_xT = abs(sol_xy[0][0])
        self.trailing_ellipse_yT = abs(sol_xy[0][1])
    
    def __repr__(self):
        return "Foil Geometry Parameters: \n \
        chord length [M] : % s \n \
        leading edge height [M] : % s \n \
        leading edge width : % s \n \
        trailing edge height [M] : % s \n \
        trailing edge width : % s \n \
        " % (self.chord, self.leading_ellipse_y, self.leading_ellipse_x, self.trailing_ellipse_y, self.trailing_ellipse_x)

      
class FoilProf(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, f, h0, theta0, chord, steps_per_cycle, total_cycles=4, density=1.225):
        self.freq = f                    
        self.theta0 = np.radians(theta0)
        self.steps_per_cycle = steps_per_cycle
        self.dt = 1/(f*steps_per_cycle)
        self.T = round(total_cycles/f,6)
        self.rho = density                          #fluid density
        self.chord = chord
        self.h0 = h0
        samp = int(np.ceil(self.T/self.dt) + 1)     #total number of time steps 
        self.time = [0]*samp
        self.h = [0]*samp
        self.theta = [0]*samp
        for x in range(samp):
            ti = round(x*self.dt,5)
            self.time[x] = ti
            self.h[x] = self.h0*cos(2*pi*x/steps_per_cycle)
            self.theta[x] = self.theta0*cos(2*pi*x/steps_per_cycle+pi/2)
            ## These are the heaving and pitching rates
            #self.h_dot[x] = 2*pi*f*self.h0*cos(2*pi*f*ti+pi/2)
            #self.theta_dot[x] = 2*pi*f*self.theta0*cos(2*pi*f*ti)

            
if __name__ == "__main__":
    """testing script functionality"""

    k = FoilProf(1.6,0.15/2,70,0.15,1000,4)
    plt.plot(k.time, k.h, label = "heaving velocity")
    #plt.plot(k.time, k.theta, label = "pitching velocity")
    plt.xlabel('time [s]')
    plt.legend()
    #plt.show()
    print()
    
    check = FoilGeo()
    # print(check.leading_ellipse_xT)
    # print(check.trailing_ellipse_xT)
    # print(check.leading_ellipse_yT)
    # print(check.trailing_ellipse_yT)

