import os, sys
import subprocess
import shutil
import numpy as np

MainCodePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(MainCodePath)
import InputForm as inp

path = inp.sim_path + "\\" + inp.folder_name

parameter_search = np.array([inp.chord_length, inp.leading_edge_width/inp.leading_edge_height, inp.trailing_edge_height, inp.trailing_edge_width/inp.trailing_edge_height, inp.leading_edge_height])
MeshGen_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFileGeomMesh.wbjn", "r").readlines()
#for param in parameter_search:
 #   MeshGen_file = [w.replace(param[1], param[0]).strip() for w in MeshGen_file]

p = 0
count = -1
for line in MeshGen_file:
    count += 1
    if p == 1:
        MeshGen_file[count] = MeshGen_file[count].replace('Expression="', 'Expression="' + str(parameter_search[int(param)-1]))
        p = 0
    if line.find("Parameter=parameter") > 0:
        p = 1
        param = line[-3]

with open(path + "\\" + inp.folder_name + "_genFileGeomMesh_Script.wbjn", "w") as new_wbjn_file:
    for lineitem in MeshGen_file:
        new_wbjn_file.write('%s' % lineitem)


fluent_path = shutil.which("fluent")
WB_path=fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"
subprocess.Popen([WB_path, '-R', 'WB_genFileGeomMesh.wbjn', '-I'])

# worDir = os.getcwd()


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen