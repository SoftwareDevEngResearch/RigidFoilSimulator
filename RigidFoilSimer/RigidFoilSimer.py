import RigidFoilSimer.FoilParameters as FP
import AnsysFiles.talkToAnsys as TA
import DataProcessing as DP
import InputForm as inp

import shutil

def yesNo(prompt):
    if FP.FoilParameters.query_yes_no(prompt) == False:
        sys.exit("Done.")

def main():
    """Runs simulation from reading in input form to processing end data"""

    ## Establish paths that are referenced throughout the package
    folder_path = inp.sim_path + "\\" + inp.folder_name
    project_path = folder_path + "\\" + inp.project_name
    wbjnMesh_path = project_path + "_genFileGeomMesh.wbjn"
    wbjnFluent_path = project_path + "_genFileFluent.wbjn"
    FFF_path =  project_path + "_files\dp0\FFF\Fluent"

    fluent_path = shutil.which("fluent")
    WB_path = fluent_path[0:int(fluent_path.find("fluent"))] + r"Framework\bin\Win64\RunWB2.exe"
  
    ## Reading in input form
    FoilGeo = FP.FoilParameters.FoilGeo(inp.chord_length, inp.leading_edge_height, inp.leading_edge_width, inp.trailing_edge_height, inp.trailing_edge_width)
    FoilDyn = FP.FoilParameters.FoilDynamics(inp.reduced_frequency, inp.heaving_frequency, inp.heaving_amplitude, inp.pitching_amplitude, inp.chord_length, inp.time_steps_per_cycle, inp.number_of_cycles, inp.fluid_density)

    ## Generate C File
    FP.CFile_Generation.genCFile(folder_path, FoilGeo, FoilDyn)

    ## Generate Mesh Files
    TA.generateMesh_wbjn(project_path, wbjnMesh_path)
    yesNo("Generate project file and mesh file?")
    TA.run_wbjn(WB_path, wbjnMesh_path, '-B')

    ## Generate Fluent Files
    yesNo("Project with Mesh file has been generated. Begin simulation? (This will take a long time)")
    TA.generateFluent_wbjn(folder_path, project_path, wbjnFluent_path, FoilDyn)
    TA.run_wbjn(WB_path, wbjnFluent_path, '-B')

    ## Process Wall shear data
    DP.processWallshear.process_wallshear_data(FFF_path, FoilDyn)
    
if __name__ == "__main__":
    main()