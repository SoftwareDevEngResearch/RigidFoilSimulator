import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve
import sys, os


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
        
        ## These equations are necessary if you decide to switch to SpaceClaim Geometry Scripting. 
        ## These are not required for parameterization
        # #Solve for tangent lines to the leading and trailing edge ellipses
        # m, k = symbols('m k')
        # eq1 = Eq((self.leading_ellipse_x**2*k*m - self.leading_ellipse_origin*self.leading_ellipse_y**2)**2 - (self.leading_ellipse_y**2+self.leading_ellipse_x**2*m**2)*(self.leading_ellipse_origin**2*self.leading_ellipse_y**2+self.leading_ellipse_x**2*k**2-self.leading_ellipse_y**2*self.leading_ellipse_x**2),0)
        # eq2 = Eq((self.trailing_ellipse_x**2*k*m - self.trailing_ellipse_origin*self.trailing_ellipse_y**2)**2 - (self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*m**2)*(self.trailing_ellipse_origin**2*self.trailing_ellipse_y**2+self.trailing_ellipse_x**2*k**2-self.trailing_ellipse_y**2*self.trailing_ellipse_x**2),0)
        # sol_dict = solve((eq1,eq2),(m,k))
        
        # # Define the equation for tangent lines
        # x, y = symbols('x y')
        # eqT = Eq(sol_dict[1][0]*x+sol_dict[1][1]-y,0)
        
        # # Solve for the intersection point at the leading edge ellipse
        # eqE = Eq((x-self.leading_ellipse_origin)**2/self.leading_ellipse_x**2 + y**2/self.leading_ellipse_y**2 - 1,0)
        # sol_xy = solve((eqT,eqE),(x,y))
        # self.leading_ellipse_xT = abs(sol_xy[0][0])
        # self.leading_ellipse_yT = abs(sol_xy[0][1])
        
        # # Solve for the intersection point at the trailing edge ellipse
        # eqE = Eq((x-self.trailing_ellipse_origin)**2/self.trailing_ellipse_x**2 + y**2/self.trailing_ellipse_y**2 - 1,0)
        # sol_xy = solve((eqT,eqE),(x,y))
        # self.trailing_ellipse_xT = abs(sol_xy[0][0])
        # self.trailing_ellipse_yT = abs(sol_xy[0][1])
    
    def __repr__(self):
        return "Foil Geometry Parameters [M]: \n \
        chord length : \t\t % s \n \
        leading edge height : \t\t % s \t\t\n \
        leading edge width : \t\t % s \t\t\n \
        trailing edge height : \t % s \t\t\n \
        trailing edge width : \t\t % s \t\t\n \
        " % (self.chord, self.leading_ellipse_y, self.leading_ellipse_x, self.trailing_ellipse_y, self.trailing_ellipse_x)

      
class FoilDynamics(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, k, f, h0, theta0, chord, steps_per_cycle, total_cycles=4, density=1.225):
        self.reduced_frequency = k
        self.freq = f                    
        self.theta0 = np.radians(theta0)
        self.steps_per_cycle = steps_per_cycle
        self.dt = 1/(f*steps_per_cycle)
        self.T = round(total_cycles/f,6)
        self.rho = density                          #fluid density
        self.chord = chord
        self.velocity_inf = f*chord/k
        self.h0 = h0
        samp = int(np.ceil(self.T/self.dt) + 1)     #total number of time steps 
        self.time = [0]*samp
        self.h = [0]*samp
        self.theta = [0]*samp
        for x in range(samp):
            ti = round(x*self.dt,5)
            self.time[x] = ti
            self.h[x] = self.h0*cos(2*pi*x/steps_per_cycle)-self.h0
            self.theta[x] = self.theta0*cos(2*pi*x/steps_per_cycle+pi/2)
            ## These are the heaving and pitching rates
            #self.h_dot[x] = 2*pi*f*self.h0*cos(2*pi*f*ti+pi/2)
            #self.theta_dot[x] = 2*pi*f*self.theta0*cos(2*pi*f*ti)


def query_yes_no(question, default=None):
    """Ask a yes/no question via input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def path_check(path, prompt):
    """figure out whether file exists and if so, how to handle it"""
    while True:
        data = input(prompt)
        if data.lower() not in ('a', 'b', 'c'):
            print("Not an appropriate choice.")
        elif data.lower()=='a':
            try:
                os.mkdir(path)
            except OSError:
                #print ("Creation of the directory %s failed" % path)
                if os.path.exists(path):
                    if query_yes_no("Folder already exists, is it okay to replace existing files?")==False:
                        path = input("Enter the full path of the folder you would like the *.c file to be saved w/o quotations: ")
                        path_check(path)
                    else:
                        break
                else:    
                    sys.exit("Directory for the simulation files could not be created/processed. Please check your directory inputs in the input form")
            else:
                print ("Successfully created the directory %s " % path)
            break
        elif data.lower()=='b':
            path = input("Enter the full path of the folder you would like the *.c file to be saved w/o quotations: ")
            break
        elif data.lower()=='c':
            sys.exit("User defined function needs to be generated and stored somewhere to proceed")
    return path
            
            
if __name__ == "__main__":
    """testing script functionality"""

    check = FoilGeo()
    print(check)
    
    k = FoilDynamics(1.6,check.chord/2,70,check.chord,1000,4)
    plt.plot(k.time, k.h, label = "heaving velocity")
    #plt.plot(k.time, k.theta, label = "pitching velocity")
    plt.xlabel('time [s]')
    plt.legend()
    # plt.show()
    

