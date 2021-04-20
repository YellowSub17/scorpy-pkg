#!/usr/bin/env python3
'''
corr-comp.py

Compare various correlation vols
'''



import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np


extent = 'default'

nq = 20
ntheta = 36




qmax = None
cif = scorpy.CifData('../data/xtal/homebrew-sf.cif', qmax=qmax)

# qmax = 2*0.18496491731629183/3
# cif = scorpy.CifData('../data/xtal/1al1-sf.cif', qmax=qmax)

# print(cif.spherical)
# cif.bin_spherical(nq,ntheta,ntheta)
# print(cif.spherical)


cor1 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
cor1.correlateSPH(cif.spherical)


cif.bin_spherical(nq,ntheta,ntheta)


cor2 = scorpy.CorrelationVol(nq,ntheta, cif.qmax)
cor2.correlateSPH(cif.spherical)



cor1.plot_sumax(extent=extent)
plt.title('sum before bin')

cor2.plot_sumax(extent=extent)
plt.title('sum after bin')


plt.show()





















