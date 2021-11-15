#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import numpy as np

@jit
def f(x,y,z):
    prd = 15.
    r = (((x+0)%33.3 -16.67)**2 + ((y+16.67)%33.3 -16.67)**2)**0.5
    rd = r - prd
    base =12.**2> (x - ((x if x < 100. else 100.) if x > -100. else -100.))**2\
                 +(y - ((y if y <  50. else  50.) if y >  -50. else  -50.))**2\
                 +(z - ((z if z <   0. else   0.) if z >   -0. else   -0.))**2
    hole = (12**2 < rd**2 + z**2) and (prd**2 > r**2)
    return base and not hole


render.renderAndSave(f, 'airmat.stl', 1)

