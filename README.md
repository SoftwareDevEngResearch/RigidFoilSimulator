# RigidFoilSimulator
Python-based oscillating rigid foil simulation package enables novice users to get meaningful computational fluid dynamics results through a streamlined command line interface. 

## Installation
This package can be installed via:

    pip install git+https://github.com/vickie-ngo/RigidFoilSimulator

## Prerequisites
The simulation itself is ran through the ANSYS Workbench software package and therefore relies on the successful installation of ANSYS and its dependencies. Some of the dependencies include:
  1. This package was developed using Windows, use with caution when working on other systems
  2. ANSYS 2019 or later
  3. Visual Studio
  4. Git
  
## Warnings and Limitations
It not recommended to run the Rigid Foil Simulator package without prior working knowledge of how computational fluid dynamics is performed. Output results should be analyzed with discretion before being used to expand and inform on scientific understanding.

## Usage Example
To use the rigid foil simulation package, start by defining the 3 class objects to your workspace:
    
    from RigidFoilSimer import Parameters
    
    filepaths = Parameters.FilePath(r <path to folder*> )
    Geo = Parameters.Geometry()
    Dyn = Parameters.Dynamics()

\* for example, "C:\Users\<username>\Desktop" will save an example folder to the desktop

### Option #1: Running Code Beginning to End
Import the main code module to the workspace and add the module statement:

    from RigidFoilSimer import RigidFoilSimer
    
    RigidFoilSimer.main(filepaths, Geo, Dyn)

**If ANSYS is not installed,** the example case will create an example folder and store all new files into the folder. The example will proceed to run an example case of post-processing on existing data to show what the output would look if the simulation had been completed.

**If ANSYS is installed,** the example case will do the same things as stated previously, but will also run the first 10 time steps of the simulation within ANSYS (note: post-processing of the example does not use data generated from the example simulation, as simulations take over 10hrs of run time to reach the time of interest)

### Option #2: Create C-File
Import the CFile_Generation module and add the module statement:

    from RigidFoilSimer import CFile_Generation
    
    CFile_Generation.genCFile(filepaths, Geo, Dyn)

A \*.c file will be generated in the defined folder.
