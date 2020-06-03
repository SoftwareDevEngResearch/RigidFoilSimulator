import os, sys
import subprocess
import shutil
import numpy as np

MainCodePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(MainCodePath)
import InputForm as inp
import FoilParameters as fP

def getTasks(name):
    r = os.popen('tasklist /v').read().strip().split('\n')
    print ('# of tasks is %s' % (len(r)))
    for i in range(len(r)):
        s = r[i]
        if name in r[i]:
            print ('%s in r[i]' %(name))
            return r[i]
    return []
    



# folder_path = inp.sim_path + "\\" + inp.folder_name
# project_path = folder_path + "\\" + inp.project_name + ".wbpj"

# MeshGen_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFileGeomMesh.wbjn", "r").readlines()

# file_search = np.array([['Open(FilePath="'+os.path.dirname(os.path.abspath(__file__)) + '\\WorkbenchProjectTemplate.wbpj")','Open(FilePath="")'],['FilePath="'+project_path+'",','FilePath="",']])
# for param in file_search:
    # param = [w.replace("\\","/") for w in param]
    # MeshGen_file = [w.replace(param[1], param[0]) for w in MeshGen_file]

# parameter_search = np.array([inp.chord_length, inp.leading_edge_width/inp.leading_edge_height, inp.trailing_edge_height, inp.trailing_edge_width/inp.trailing_edge_height, inp.leading_edge_height])
# p = 0
# count = -1
# for line in MeshGen_file:
    # count += 1
    # if p == 1:
        # MeshGen_file[count] = MeshGen_file[count].replace('Expression="', 'Expression="' + str(parameter_search[int(param)-1]))
        # p = 0
    # if line.find("Parameter=parameter") > 0:
        # p = 1
        # param = line[-3]

# wbjnMesh_path = folder_path + "\\" + inp.project_name + "_genFileGeomMesh.wbjn"
# with open(wbjnMesh_path, "w") as new_wbjn_file:
    # for lineitem in MeshGen_file:
        # new_wbjn_file.write('%s' % lineitem)

fluent_path = shutil.which("fluent")
WB_path=fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"
# subprocess.Popen([WB_path, '-R', wbjnMesh_path, '-I'])

# if fP.FoilParameters.query_yes_no("Project with Mesh file is being generated. After AnsysFW.exe closes, enter 'yes' to begin simulation or 'no' to exit")==False:
    # sys.exit("Done.")

# wbjnFluent_path = folder_path + "\\" + "WB_genFluent.wbjn"
# subprocess.Popen([WB_path, '-R', wbjnFluent_path, '-I'])

imgName = 'RunWB2.exe'

notResponding = 'Not Responding'

r = getTasks(imgName)

if not r:
    print('%s - No such process' % (imgName)) 

elif 'Not Responding' in r:
    print('%s is Not responding' % (imgName))
        
else:
    print('%s is Running or Unknown' % (imgName))






# worDir = os.getcwd()


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen