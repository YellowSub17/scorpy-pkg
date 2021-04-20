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
qmax = 2*0.18496491731629183/3

extent = 'default'

nq = 140
ntheta = 180




cif = scorpy.CifData('../data/xtal/homebrew-sf.cif', qmax=qmax)
cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax=qmax)


cor1 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
cor2 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)

print('correlating 3D')
cor1.correlate3D(cif.scattering)

print('correlating spherical')
cor2.correlateSPH(cif.spherical, cif)



cor1.plot_sumax(extent=extent)
plt.title('sum qxyzi')
cor2.plot_sumax(extent=extent)
plt.title('sum qtpi')

# cor1.plot_q1q2(extent=extent)
# plt.title('q1q2 qxyzi')
# cor2.plot_q1q2(extent=extent)
# plt.title('q1q2 qtpi')



plt.show()





















