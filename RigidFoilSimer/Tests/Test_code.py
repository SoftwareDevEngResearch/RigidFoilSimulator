from RigidFoilSimer import RigidFoilSimer, Parameters, processWallshear
import numpy as np
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
    
def test_processWallshear():
    folder_path = os.path.dirname(os.path.abspath(__file__))
    k = 0.12
    freq = 1.6
    chord = 0.15
    dyn = Parameters.Dynamics(k, freq, 0.075, 70, chord, 1000, 2, 1.225)
    processWallshear.wallshearData(folder_path + "\Assets", dyn)