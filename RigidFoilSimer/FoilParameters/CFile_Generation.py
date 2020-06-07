import FoilParameters.FoilParameters as fP
import sys
import os
import numpy as np

MainCodePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(MainCodePath)
import InputForm as iForm

def genCFile(folder_path, FoilGeo, FoilDyn):
    print(FoilGeo)

    if fP.query_yes_no("Are these the parameters you want to use to generate a user defined function?")== False:
        sys.exit("\nPlease enter the desired foil parameters into the input form")
    folder_path = fP.path_check(folder_path, "\nStore simulation files to %s?\nA) Yes, use/create the folder and save to it \nB) No, I want to specify an existing folder directory \nC) No, I want to cancel this process\nPick an answer of A, B, or C: " % (folder_path))

    parameter_search = np.array([[FoilGeo.chord, 'C_chord_length'], [FoilDyn.rho, 'C_fluid_density'], [FoilDyn.freq, 'C_heaving_frequency'], [FoilDyn.h0, 'C_heaving_amplitude'], [FoilDyn.theta0, 'C_pitching_amplitude'], [FoilDyn.velocity_inf, 'C_velocity_inf']])
    UDF_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\Rigid_TemPlate.c", "r").readlines()
    for param in parameter_search:
        UDF_file = [w.replace(param[1], param[0]).strip() for w in UDF_file]

    with open(folder_path + "\\modRigidPlateFile.c", "w") as new_UDF_file:
        for lineitem in UDF_file:
            new_UDF_file.write('%s\n' % lineitem)
    
    print('UDF has been generated.')
