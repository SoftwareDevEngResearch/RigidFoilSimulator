import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import symbols, Eq, solve
import sys, os
import shutil


pi = np.pi
cos = np.cos

class FilePath(object):
    """Establishes paths that are referenced throughout the package"""
    def __init__(self, folder_parentpath, folder_name="RigidFoilSimer_Example", project_name="NACA0015_Example"):
        self.folder_path = (folder_parentpath + "\\" + folder_name).replace("/","\\")
        self.folder_name = folder_name
        self.project_path = (self.folder_path + "\\" + project_name).replace("/","\\")
        self.project_name = project_name
        self.wbjnMesh_path = self.project_path + "_genFileGeomMesh.wbjn"
        self.wbjnFluent_path = self.project_path + "_genFileFluent.wbjn"
        self.data_path = self.project_path + "_files\dp0\FFF\Fluent"

        fluent_path = shutil.which("fluent")
        if fluent_path == None:
            print("Fluent application does not exist. The rest of this package will operate without interacting with live simulations until ANSYS is installed and file paths are reestablished.")
        else:
            self.WB_path = fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"
       
        if self.folder_name == "RigidFoilSimer_Example":
            self.data_path =  os.path.dirname(os.path.realpath(__file__)) + "\Tests\Assets"
    
    def newFolderPath(self, folder_path):
        self.folder_path = folder_path.replace("/","\\")
        self.project_path = (self.folder_path + "\\" + self.project_name).replace("/","\\")
        self.wbjnMesh_path = (self.project_path + "_genFileGeomMesh.wbjn").replace("\\","/")
        self.wbjnFluent_path = self.project_path + "_genFileFluent.wbjn"
        self.data_path =  self.project_path + "_files\dp0\FFF\Fluent"
        
    def __repr__(self):
        output = ("\nFile Paths: \n \
        Folder path : \t\t % s \n \
        Project name : \t % s \n \
        " % (self.folder_path, self.project_path))
        if hasattr(self, 'WB_path'):
            output = output + "Workbench path : \t % s " % (self.WB_path)
        return output

class Geometry(object):
    """Foil geometry conditions are used to explore different sizes and shapes"""
    
    def __init__(self, chord=0.15, leading_ellipse_y = 0.15*0.075, leading_ellipse_x = 0.15*0.3, trailing_ellipse_y = 0.001, trailing_ellipse_x=0.006):
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

      
class Dynamics(object):
    """Foil parameters are all parameters involved in the motion generation"""
    # class body definition
    
    def __init__(self, k=0.08, f=1.6, h0=0.075, theta0=70, chord=0.15, steps_per_cycle=1000, total_cycles=0.01, density=1.225):
        self.reduced_frequency = k
        self.freq = f                    
        self.theta0 = np.radians(theta0)
        self.steps_per_cycle = steps_per_cycle
        self.dt = 1/(f*steps_per_cycle)
        self.total_cycles = total_cycles
        #self.T = round(total_cycles/f,6)
        self.rho = density                          #fluid density
        self.chord = chord
        self.velocity_inf = f*chord/k
        self.h0 = h0
        samp = int(np.ceil(round(total_cycles/f,6)/self.dt) + 1)     #total number of time steps 
        self.total_steps = samp-1
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

    def __repr__(self):
        return "Foil Dynamic Parameters: \n \
        reduced frequency [-]: \t % s \n \
        chord length [M]: \t\t % s \n \
        heaving frequency [Hz]: \t % s \n \
        heaving amplitude [M]: \t % s \n \
        pitching amplitude [rad]: \t % s \n \
        steps per cycle [N]: \t\t %s \n \
        total cycles [-]: \t\t %s \n \
        fluid density [kg/m^3]: \t %s \n \
        " % (self.reduced_frequency, self.chord, self.freq , self.h0, self.theta0, self.steps_per_cycle, self.total_cycles, self.rho)


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
        data = input(prompt % (path))
        if data.lower() not in ('a', 'b', 'c'):
            print("Not an appropriate choice.")
        elif data.lower()=='a':
            try:
                os.mkdir(path)
            except OSError:
                #print ("Creation of the directory %s failed" % path)
                if os.path.exists(path):
                    if query_yes_no("\nFolder already exists, is it okay to replace existing files?")==False:
                        path = input("\nEnter the full path of the folder you would like the file to be saved w/o quotations: ")
                    else:
                        break
                else:    
                    sys.exit("\nDirectory for the simulation files could not be created/processed. Please check your directory inputs in the input form")
            else:
                print ("\nSuccessfully created the directory, %s " % path)
            break
        elif data.lower()=='b':
            path = input("\nEnter the full path of the folder you would like the file to be saved w/o quotations: ")
        elif data.lower()=='c':
            sys.exit("\nDirectory needs to be defined in order to proceed")
    return path
