import Parameters as FP
import AnsysFiles.talkToAnsys as TA
import DataProcessing as DP
import sys
import shutil

def yesNo(prompt):
    if FP.Parameters.query_yes_no(prompt) == False:
        sys.exit("Done.")

def main(FilePath, FoilGeo, FoilDyn):
    """Runs simulation from reading in input form to processing end data"""
  
    ## Generate C File
    FilePath = FP.CFile_Generation.genCFile(FilePath, FoilGeo, FoilDyn)

    ## Generate Mesh Files
    TA.generateMesh_wbjn(FilePath, FilePath.wbjnMesh_path, FoilGeo)
    yesNo("Generate project file and mesh file?")
    TA.run_wbjn(FilePath.WB_path, FilePath.wbjnMesh_path, '-B')

    ## Generate Fluent Files
    yesNo("Project with Mesh file has been generated. Begin simulation? (This will take a long time)")
    TA.generateFluent_wbjn(folder_path, project_path, wbjnFluent_path, FoilDyn)
    # TA.run_wbjn(WB_path, wbjnFluent_path, '-B')

    # ## Process Wall shear data
    # DP.processWallshear.process_wallshear_data(FilePath.FFF_path, FoilDyn)
    
if __name__ == "__main__":
    ## Reading in input form
    FilePaths = FP.Parameters.FilePath("C:/Users/vicki/Desktop","githubVersion")
    FoilGeo = FP.Parameters.Geometry()
    FoilDyn = FP.Parameters.Dynamics()

    main(FilePaths, FoilGeo, FoilDyn)