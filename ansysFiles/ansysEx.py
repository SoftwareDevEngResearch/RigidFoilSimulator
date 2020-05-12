# import os
# import pyansys
# from scipy import sparse

# # load the full file
# fobj = pyansys.FullReader('testFile.scscript')
# print(fobj)

# path = os.getcwd()
# ansys = pyansys.Mapdl(run_location=path, interactive_plotting=True)

# # create a square area using keypoints
# ansys.prep7()
# ansys.k(1, 0, 0, 0)
# ansys.k(2, 1, 0, 0)
# ansys.k(3, 1, 1, 0)
# ansys.k(4, 0, 1, 0)
# ansys.l(1, 2)
# ansys.l(2, 3)
# ansys.l(3, 4)
# ansys.l(4, 1)
# ansys.al(1, 2, 3, 4)
# ansys.aplot()
# ansys.save()
# ansys.exit()

import os 
os.chdir(r'C:\Users\vicki\RigidFoilUDFGenerator')

import pyansys

