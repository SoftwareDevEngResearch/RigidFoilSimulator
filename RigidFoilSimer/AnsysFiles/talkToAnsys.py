import os, sys
import subprocess
import shutil
import numpy as np

MainCodePath = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) 
sys.path.append(MainCodePath)
import InputForm as inp
import FoilParameters as fP

def getTasks(name):
    timer = 0
    ramp = 0
    tasks = []
    while tasks or ramp < 2:
        tasks = []
        r = os.popen('tasklist /v').read().strip().split('\n')
        for i in range(len(r)):
            if name in r[i]:
                tasks = r[i]
        if 'Not Responding' in tasks:
            sys.exit('Not Responding, ANSYS and Python operation will be exited')
        if tasks==[] and ramp==timer:
            ramp += 1
            print('Waiting for response')
        elif ramp==timer:
            print('%s is running...' % name)
        elif ramp!=timer:
            ramp = 10
        timer += 1

def write2file(inputList, outputFile):
    with open(outputFile, "w") as new_wbjn_file:
        for lineitem in inputList:
            new_wbjn_file.write('%s' % lineitem)
   
   
def run_wbjn(WB_path, wbjn_path, method):
    subprocess.Popen([WB_path, '-R', wbjn_path, method])
    
    getTasks('AnsysFW.exe')
    print('Operation complete.')
  

def generateMesh_wbjn(project_path, wbjnMesh_path):

    MeshGen_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFileGeomMesh.wbjn", "r").readlines()

    file_search = np.array([[os.path.dirname(os.path.abspath(__file__)) + '\\WorkbenchProjectTemplate.wbpj','InputFile'],[project_path + ".wbpj",'SaveFile']])
    for param in file_search:
        param = [w.replace("\\","/") for w in param]
        MeshGen_file = [w.replace(param[1], param[0]) for w in MeshGen_file]

    parameter_search = np.array([inp.chord_length, inp.leading_edge_width/inp.leading_edge_height, inp.trailing_edge_height, inp.trailing_edge_width/inp.trailing_edge_height, inp.leading_edge_height])
    p = 0
    for line in range(len(MeshGen_file)):
        if '_Ex_' in MeshGen_file[line]:
            MeshGen_file[line] = MeshGen_file[line].replace('_Ex_', str(parameter_search[p]))
            p += 1
            
    write2file(MeshGen_file, wbjnMesh_path)
    print('Mesh Journal has been generated.')
        
        
def generateFluent_wbjn(folder_path, project_path, wbjnFluent_path, FoilDyn):
    
    FluentGen_file = open(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFluent.wbjn", "r").readlines()
    print(os.path.dirname(os.path.abspath(__file__)) + "\\WB_genFluent.wbjn")
    
    file_item = np.array(['InputFile', '_xVelocity_','UDF_C_File','_chordLength_', '_wallShearFileName_', '_stepSize_', '_totalSteps_'])
    file_replace = np.array([(project_path + '.wbpj').replace("\\","/"), FoilDyn.velocity_inf, (folder_path + "\\modRigidPlateFile.c").replace("\\","/"), FoilDyn.chord, str(FoilDyn.reduced_frequency).replace(".","") + '-wallshear', FoilDyn.dt, FoilDyn.total_steps])
   
    for param in range(len(file_item)):
        FluentGen_file = [w.replace(file_item[param], file_replace[param]) for w in FluentGen_file]
    
    write2file(FluentGen_file, wbjnFluent_path)
    print('Fluent Simulation Journal has been generated.')