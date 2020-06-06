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
    for i in range(len(r)):
        if name in r[i]:
            print('Program is running...')
            return r[i]
    return []

def generateMesh_wbjn(folder_path, wbjnMesh_path):
    project_path = folder_path + "\\" + inp.project_name + ".wbpj"

    MeshGen_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFileGeomMesh.wbjn", "r").readlines()

    file_search = np.array([[os.path.dirname(os.path.abspath(__file__)) + '\\WorkbenchProjectTemplate.wbpj','InputFile'],[project_path,'SaveFile']])
    for param in file_search:
        param = [w.replace("\\","/") for w in param]
        MeshGen_file = [w.replace(param[1], param[0]) for w in MeshGen_file]

    parameter_search = np.array([inp.chord_length, inp.leading_edge_width/inp.leading_edge_height, inp.trailing_edge_height, inp.trailing_edge_width/inp.trailing_edge_height, inp.leading_edge_height])
    print(parameter_search.shape)
    Expressions = np.array(range(5)).astype(str)
    print(Expressions.shape)
    New = np.append(parameter_search, Expressions, axis=1)
    print(New)
    
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
    print(MeshGen_file)
    
    # with open(wbjnMesh_path, "w") as new_wbjn_file:
        # for lineitem in MeshGen_file:
            # new_wbjn_file.write('%s' % lineitem)

def generateMesh_msh(WB_path, wbjnMesh_path):
    subprocess.Popen([WB_path, '-R', wbjnMesh_path, '-B'])

    imgName = 'AnsysFW.exe'
    timer = 0
    ramp = 0
    r = getTasks(imgName)
    while r or ramp < 2:
        if 'Not Responding' in r or timer > 10000000:
            sys.exit('Not Responding, ANSYS and Python operation will be exited')
        if False and ramp==timer:
            ramp += 1
            print('Waiting for response')
        elif ramp!=timer:
            ramp = 10
        timer += 1
        r = getTasks(imgName)
        
    
folder_path = inp.sim_path + "\\" + inp.folder_name
fluent_path = shutil.which("fluent")
WB_path = fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"
wbjnMesh_path = folder_path + "\\" + inp.project_name + "_genFileGeomMesh.wbjn"

generateMesh_wbjn(folder_path, wbjnMesh_path)
# generateMesh_msh(WB_path, wbjnMesh_path)

# if fP.FoilParameters.query_yes_no("Project with Mesh file has been generated. Begin simulation?")==False:
    # sys.exit("Done.")

# wbjnFluent_path = folder_path + "\\" + "WB_genFluent.wbjn"
# subprocess.Popen([WB_path, '-R', wbjnFluent_path, '-I'])



# worDir = os.getcwd()


# # allCmds = "{}; {}".format(cmd1 cmd2)
# # allCmds = "{}; {}".format(cmd1, cmd2) 
# # https://stackoverflow.com/questions/9649355/python-how-to-run-multiple-commands-in-one-process-using-popen