from RigidFoilSimer import Parameters, talkToAnsys, CFile_Generation, processWallshear
import matplotlib.pyplot as plt
import sys
import shutil

def yesNo(prompt):
    if Parameters.query_yes_no(prompt) == False:
        sys.exit("Done.")

def main(FilePath, FoilGeo, FoilDyn):
    """Runs simulation from reading in input form to processing end data"""
  
    ## Generate C File
    FilePath = CFile_Generation.genCFile(FilePath, FoilGeo, FoilDyn)

    ## Generate Journal Files
    talkToAnsys.generateMesh_wbjn(FilePath, FoilGeo, 1)
    talkToAnsys.generateFluent_wbjn(FilePath, FoilDyn, 1)

    if hasattr(FilePath, 'WB_path'):
        talkToAnsys.run_wbjn(FilePath.WB_path, FilePath.wbjnMesh_path, '-B')
        yesNo("Project with Mesh file has been generated. Begin simulation? (This will take a long time)")
        talkToAnsys.run_wbjn(FilePath.WB_path, FilePath.wbjnFluent_path, '-B')

    processWallshear.wallshearData(FilePath, FoilDyn, FoilGeo)
