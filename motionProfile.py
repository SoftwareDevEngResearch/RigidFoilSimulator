import numpy as np



def test_MF_Motion():
    #f = 1.6
    #theta0 = 
    theta0 = math.radians(70)
    return theta0

def MF_motion(f, theta0, h0, dt, t):
	'''Use heaving and  pitching amplitudes to predict foil main body motion'''
	vel = 2*f*h0*cos(2*pi*f*t+pi/2)
	theta = 2*pi*f*theta0*cos(2*pi*f*t)
	return