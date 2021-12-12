import numpy as np

def POLAR(tup, ang):
    r = tup[0]
    theta = tup[1]
    x = r * np.cos(theta + ang)
    y = r * np.sin(theta + ang)    
    return (x, y)