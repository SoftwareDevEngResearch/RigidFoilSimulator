from RigidFoilSimer import RigidFoilSimer, Parameters, processWallshear, CFile_Generation, talkToAnsys
import numpy as np
import subprocess
import pytest
import os

def test_Geometry():
    geo = Parameters.Geometry(0.15,0.15*0.075, 0.15*0.3,0.001,0.006)
    assert geo.chord == 0.15
    assert np.allclose(geo.trailing_ellipse_origin, 0.069)
    
def test_Dynamics():
    k = 0.08
    freq = 1.6
    chord = 0.15
    dyn = Parameters.Dynamics(k, freq, 0.075, 70, chord, 1000, 1, 1.225)
    assert dyn.velocity_inf == freq*chord/k
    assert np.allclose(dyn.theta[250], -dyn.theta0)
    assert np.allclose(dyn.theta[1000], 0)

def test_genCFile(tmp_path):
    dyn = Parameters.Dynamics()
    geo = Parameters.Geometry()
    d = tmp_path / "sub"
    d.mkdir()
    #p = d / "hello.txt"
    #p.write_text("Stuff in txt file")
    folder_path = Parameters.FilePath(str(d))
    UDF = CFile_Generation.genCFile(folder_path, geo, dyn)

def test_processWallshear():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    k = 0.12
    freq = 1.6
    chord = 0.15
    time_step = 1130
    vortex_xC = 0.053220586717218   #vortex_xC is the x position relative to the chord length that the vortex is being shed
    dyn = Parameters.Dynamics(k, freq, 0.075, 70, chord, 1000, 2, 1.225)
    output = processWallshear.wallshearData(folder_path + r"\Assets", dyn)
    assert output[0] == time_step
    assert np.allclose(output[1], vortex_xC)
