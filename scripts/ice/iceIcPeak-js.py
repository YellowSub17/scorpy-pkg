#!/usr/bin/env python

import numpy as N
import math as M
from numpy import linalg as LA
import h5py as H
import glob as G
import os 
import re
import pylab as P
#from myModules import extractDetectorDist as eDD

# hexagonal ice peaks
HIceQ = {'100':1.611, '002':1.717, '101':1.848, '102':2.353,
		 '110':2.793, '103':3.035,
		 '200':3.222, '112':3.272, '201':3.324}
#hkl = [[1,0,0], [0,0,2], [1,0,1], [1,0,2], [1,1,0], [1,0,3], [2,0,0], [1,1,2], [2,0,1]]


#		numQLabels = len(HIceQ.keys())+1
#		labelPosition = maxAngAvg/numQLabels
#		for i,j in HIceQ.iteritems():
#			labelPosition = HIceP[i]*maxAngAvg/numQLabels
#			P.axvline(j, 0, colmax, color='k', ls='--')
#			P.text(HIceQLabel[i], labelPosition, str(i), rotation="45")
#

#a = 4.518 #in A
#c = 7.356 #in A
d = 6.358

#b1 = N.array([2*M.pi/(a*M.sqrt(3)), 2*M.pi/a, 0])
#b2 = N.array([-2*M.pi/(a*M.sqrt(3)), 2*M.pi/a, 0])
#b3 = N.array([0, 0, 2*M.pi/c])
b1 = N.array([2*M.pi/d, 0, 0])
b2 = N.array([0, 2*M.pi/d, 0])
b3 = N.array([0, 0, 2*M.pi/d])

reflections = []
hkl = []

for h in range(-4, 5):
    for k in range(-4, 5):
        for l in range(-4, 5):
            if (h == 0 and k == 0 and l == 0):
                    continue
            #if (((abs(h) + abs(k) + abs(l))%4 == 0) or ((abs(h) + abs(k) + abs(l))%4 == 1)) and ((abs(h)%2 == abs(k)%2) and (abs(k)%2 == abs(l)%2)):
            if ((((abs(h) + abs(k) + abs(l))%4 == 0) and abs(h)%2 == 0) or abs(h)%2 == 1) and ((abs(h)%2 == abs(k)%2) and (abs(k)%2 == abs(l)%2)):
                G = h*b1 + k*b2 + l*b3
                q = M.sqrt(G[0]*G[0] + G[1]*G[1] + G[2]*G[2])
                #print "(%d %d %d) = %f A-1" % (h, k, l, q)
                reflections.append(q)
                hkl.append("(%d %d %d)" % (h, k, l))
            #if ((h == 0 and k == 0 and l == 0) or (abs((h*2 + k))%3 == 0 and abs(l)%2 == 1)):
            #    continue
            #else:
            #    G = h*b1 + k*b2 + l*b3
            #    q = M.sqrt(G[0]*G[0] + G[1]*G[1] + G[2]*G[2])
            #    #print "(%d %d %d) = %f A-1" % (h, k, l, q)
            #    reflections.append(q)
            #    hkl.append("(%d %d %d)" % (h, k, l))


peaks = set(reflections)
npeaks = len(peaks)
ordering = N.array(reflections).argsort()
orderedReflections = N.array(reflections)[ordering]
orderedhkl = N.array(hkl)[ordering]

print "Npeaks = %d" % (npeaks)
i = 0
for q in orderedReflections:
    print orderedhkl[i] + " = %f A-1" % (q)
    i += 1

#index = 0
#for x in range(npeaks):
#    q = peaks.pop()
#    n = 0
#    while orderedReflections[index]
