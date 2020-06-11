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

#### Option #1: Running Code Beginning to End
Add the main code module to the workspace and add the module statement:

    from RigidFoilSimer import RigidFoilSimer
    
    RigidFoilSimer.main(filepaths, Geo, Dyn)

**If ANSYS is not installed,** the example case will create an example folder and store all new files into the folder

#### Option #2: Create C-File
Add the CFile_Generation module

