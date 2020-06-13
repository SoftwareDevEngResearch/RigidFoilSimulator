import sys
from RigidFoilSimer import Parameters
from RigidFoilSimer import RigidFoilSimer
## Reading in input form
FilePaths = Parameters.FilePath("C:/Users/vicki/Desktop","githubVersion")
FoilGeo = Parameters.Geometry()
FoilDyn = Parameters.Dynamics()
RigidFoilSimer.main(FilePaths, FoilGeo, FoilDyn)