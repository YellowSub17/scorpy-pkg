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


# sph = scorpy.SphHarmHandler(nq,nl, qmax)
# sph.fill_from_cif(cif)
# blqq2 = scorpy.BlqqVol(nq,nl,qmax)
# blqq2.fill_from_sph(sph)


lam, u  = blqq1.get_eig()

plt.figure()
plt.plot(lam[:,0])
plt.show()


# blqq3 = scorpy.BlqqVol(nq,nl,qmax)

# for l in range(0, nl, 2):
    # lam1 = lam[:,l]
    # u1 = u[...,l]

    # x = np.matmul(u1, np.diag(lam1))
    # blqq3.vol[...,l] = np.matmul(x, np.linalg.inv(u1))




# blqq1.plot_slice(2,6)
# plt.title('Correlation Blqq')
# blqq2.plot_slice(2,6)
# plt.title('Spherical Harmonics Blqq')
# blqq3.plot_slice(2,6)
# plt.title('Corr. Eigen Recon Blqq')












# plt.show()







