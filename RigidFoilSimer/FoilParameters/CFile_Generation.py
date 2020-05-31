##RIGID-FOIL-SIMULATION-GENERATOR

## Enter directory folder name to save Simulation Files
sim_path = r"C:\Users\vicki\Desktop"
folder_name = r"RigidFoilSimulation"


## Enter foil geometry details in units of [M]

chord_length = 0.15            
leading_edge_height = 0.00325  
leading_edge_width = chord_length/4
trailing_edge_height = 0.0002  
trailing_edge_width = 0.012


## Enter dynamic parameter details

reduced_frequency = 0.08                #[-]
heaving_frequency = 1.6                 #[Hz]
heaving_amplitude = chord_length*0.5    #[M]
pitching_amplitude = 70                 #[deg]
time_steps_per_cycle = 1000             #[-]
number_of_cycles = 4                    #[-]
fluid_density = 1.225                   #[kg/m^3]

################################################################################


import FoilParameters.FoilParameters as fP
import sys
import os
import numpy as np

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

def path_check(path):
    """figure out whether file exists and if so, how to handle it"""
    while True:
        data = input("\nStore simulation files to %s?\nA) Yes, use/create the folder and save to it \nB) No, I want to specify an existing folder directory \nC) No, I want to cancel this process\nPick an answer of A, B, or C: " % (path))
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
                    sys.exit("Directory for the simulation files could not be created/processed")
            else:
                print ("Successfully created the directory %s " % path)
            break
        elif data.lower()=='b':
            path = input("Enter the full path of the folder you would like the *.c file to be saved w/o quotations: ")
            break
        elif data.lower()=='c':
            sys.exit("User defined function needs to be generated and stored somewhere to proceed")
    return path

FoilGeo = fP.FoilGeo(chord_length, leading_edge_height, leading_edge_width, trailing_edge_height, trailing_edge_width)
print(FoilGeo)

if query_yes_no("Are these the parameters you want to use to generate a user defined function?")== False:
    sys.exit("\nPlease enter the desired foil parameters into %s" % os.path.basename(__file__))

path = sim_path+"\\"+folder_name    
path = path_check(path)

FD = fP.FoilDynamics(reduced_frequency, heaving_frequency, heaving_amplitude, pitching_amplitude, chord_length, time_steps_per_cycle, number_of_cycles, fluid_density)

parameter_search = np.array([[chord_length, 'C_chord_length'], [fluid_density, 'C_fluid_density'], [heaving_frequency, 'C_heaving_frequency'], [heaving_amplitude, 'C_heaving_amplitude'], [FD.theta0, 'C_pitching_amplitude'], [FD.velocity_inf, 'C_velocity_inf']])
UDF_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\Rigid_TemPlate.c", "r").readlines()
for param in parameter_search:
    UDF_file = [w.replace(param[1], param[0]).strip() for w in UDF_file]

with open(path + "\\modRigidPlateFile.c", "w") as new_UDF_file:
    for lineitem in UDF_file:
        new_UDF_file.write('%s\n' % lineitem)
