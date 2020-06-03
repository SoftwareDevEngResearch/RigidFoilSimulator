import FoilParameters.FoilParameters as fP
import sys
import os
import numpy as np

MainCodePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(MainCodePath)
import InputForm as iForm

FoilGeo = fP.FoilGeo(iForm.chord_length, iForm.leading_edge_height, iForm.leading_edge_width, iForm.trailing_edge_height, iForm.trailing_edge_width)
print(FoilGeo)

if fP.query_yes_no("Are these the parameters you want to use to generate a user defined function?")== False:
    sys.exit("\nPlease enter the desired foil parameters into the input form")

path = iForm.sim_path+"\\"+iForm.folder_name    
path = fP.path_check(path, "\nStore simulation files to %s?\nA) Yes, use/create the folder and save to it \nB) No, I want to specify an existing folder directory \nC) No, I want to cancel this process\nPick an answer of A, B, or C: " % (path))

FD = fP.FoilDynamics(iForm.reduced_frequency, iForm.heaving_frequency, iForm.heaving_amplitude, iForm.pitching_amplitude, iForm.chord_length, iForm.time_steps_per_cycle, iForm.number_of_cycles, iForm.fluid_density)

parameter_search = np.array([[FoilGeo.chord, 'C_chord_length'], [iForm.fluid_density, 'C_fluid_density'], [iForm.heaving_frequency, 'C_heaving_frequency'], [iForm.heaving_amplitude, 'C_heaving_amplitude'], [FD.theta0, 'C_pitching_amplitude'], [FD.velocity_inf, 'C_velocity_inf']])
UDF_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\Rigid_TemPlate.c", "r").readlines()
for param in parameter_search:
    UDF_file = [w.replace(param[1], param[0]).strip() for w in UDF_file]

with open(path + "\\modRigidPlateFile.c", "w") as new_UDF_file:
    for lineitem in UDF_file:
        new_UDF_file.write('%s\n' % lineitem)
