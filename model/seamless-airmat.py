#!/usr/bin/env python3

from multiprocessing import Process

from xyzcad import render
from numba import jit
import numpy as np

@jit
def airmat(x,y,z):
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

@jit
def moldu(x,y,z):
    plm = 150
    pwm = 115
    phm = 30
    if      x < plm/2 +20 and x > -plm/2 \
        and y < 25 and y > -25 \
        and z < 0     and z > -phm/2:
        return not airmat(x,y,z)
    if      x < plm/2 and x > -plm/2 \
        and y < pwm/2 and y > -pwm/2 \
        and z < 0     and z > -phm/2:
        return not airmat(x,y,z)

    if z > 0 and z < 4 and \
        ((x+50/6)%(50/3)-(50/6))**2 + ((y+50/6)%(50/3)-(50/6))**2 < (4-z)**2:
        return not airmat(x,y,z)
    return False

@jit
def moldo(x,y,z):
    plm = 150
    pwm = 115
    phm = 30
    if z > 0 and z < 6 and \
        ((x+50/6)%(50/3)-(50/6))**2 + ((y+50/6)%(50/3)-(50/6))**2 < 4**2:
        return False
    if      x < plm/2 +20 and x > -plm/2 \
        and y < 25 and y > -25 \
        and z < phm/2     and z > 0:
        return not airmat(x,y,z)
    if      x < plm/2 and x > -plm/2 \
        and y < pwm/2 and y > -pwm/2 \
        and z < phm/2 and z > 0:
        return not airmat(x,y,z)

    return False

if __name__ == '__main__':
    #render.renderAndSave(mold2,'mold2.stl',1)
    p1 = Process(target=render.renderAndSave, args=(airmat,'airmat.stl',0.3,))
    p2 = Process(target=render.renderAndSave, args=(moldu,'moldu.stl',0.3,))
    p3 = Process(target=render.renderAndSave, args=(moldo,'moldo.stl',0.3,))
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()


#render.renderAndSave(airmat, 'airmat.stl', 1)
#render.renderAndSave(mold, 'mold.stl', 1)

