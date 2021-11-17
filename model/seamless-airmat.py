#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import numpy as np

@jit
def f(x,y,z):
    pl = 100
    pw = 66.7
    ph = 8
    nl = 3
    nw = 2
    pre = 9
    pvl = 50
    pvr = 10
    prd = 15
    r = (((x+pl/nl/2*(nl%2))%(pl/nl)-(pl/nl/2))**2 +
            ((y+pw/nw/2*(nw%2))%(pw/nw)-(pw/nw/2))**2)**0.5
    rd = r - prd
    base =pre**2> (x - ((x if x < pl/2 else pl/2) if x > -pl/2 else -pl/2))**2\
                 +(y - ((y if y < pw/2 else pw/2) if y > -pw/2 else -pw/2))**2\
                 +(z - ((z if z < ph/2 else ph/2) if z > -ph/2 else -ph/2))**2
    hole = (pre**2 < rd**2 + (z - ((z if z < ph/2 else ph/2) if z > -ph/2 else -ph/2))**2) and (prd**2 > r**2)
    valve = (y**2 + z**2) < pvr**2 and x > pl/2 and x < pl/2 + pvl
    return base and not hole or valve


render.renderAndSave(f, 'airmat.stl', 1)

