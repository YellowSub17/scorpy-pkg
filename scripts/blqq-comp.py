#!/usr/bin/env python3
'''
blqq-comp.py

Calculate the blqq matrix with various methods and compare the results.
'''



import scorpy
import matplotlib.pyplot as plt
import numpy as np






nq = 100
ntheta = 180
qmax = 0.15
nl = 37





cif = scorpy.CifData('../data/xtal/1al1-sf.cif',qmax=qmax)

correl = scorpy.CorrelationVol(nq,ntheta,qmax)
correl.correlate(cif.scattering)

blqq1 = scorpy.BlqqVol(nq,nl,qmax)
blqq1.fill_from_corr(correl)


sph = scorpy.SphHarmHandler(nq,nl, qmax)
sph.fill_from_cif(cif)
blqq2 = scorpy.BlqqVol(nq,nl,qmax)
blqq2.fill_from_sph(sph)


blqq1.plot_slice(2,6)
blqq2.plot_slice(2,6)

plt.show()







