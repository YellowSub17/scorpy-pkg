#!/usr/bin/env python3
'''
corr-comp.py

Compare various correlation vols
'''



import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np

qmax = None
extent = 'default'

nq = 20
ntheta = 36




cif = scorpy.CifData('../data/xtal/homebrew-sf.cif', qmax=qmax)

cor1 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
cor2 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)



cor1.correlate3D(cif.scattering)
cor2.correlateSPH(cif.spherical)


cor1.plot_sumax(extent=extent)
plt.title('sum qxyzi')
cor2.plot_sumax(extent=extent)
plt.title('sum qtpi')

cor1.plot_q1q2(extent=extent)
plt.title('q1q2 qxyzi')
cor2.plot_q1q2(extent=extent)
plt.title('q1q2 qtpi')



plt.show()





















