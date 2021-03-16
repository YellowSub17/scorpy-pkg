#!/usr/bin/env python3
'''
blqq-comp.py

Calculate the blqq matrix with various methods and compare the results.
'''



import scorpy
import matplotlib.pyplot as plt
import numpy as np





cor = scorpy.CorrelationVol(path='../data/dbins/1al1_qcor')
cif = scorpy.CifData('../data/xtal/1al1-sf.cif',qmax=cor.qmax)
blqq1 = scorpy.BlqqVol(cor.nq, 17, cor.qmax, comp=True)
blqq1.fill_from_corr(cor)
lam1, u1 = blqq1.get_eig(herm=False)


sph2 = scorpy.SphHarmHandler(cor.nq, 17, cor.qmax, comp=True)
sph2.fill_from_cif(cif)
blqq2 = scorpy.BlqqVol(cor.nq, 17, cor.qmax, comp=True)
blqq2.fill_from_sph(sph2)
lam2, u2 = blqq2.get_eig(herm=False)

iv3 = scorpy.SphInten(cor.nq, 2**5, cor.qmax)
iv3.fill_from_cif(cif)
sph3 = scorpy.SphHarmHandler(cor.nq,17,cor.qmax, comp=True)
sph3.fill_from_ivol(iv3)
blqq3 = scorpy.BlqqVol(cor.nq, 17, cor.qmax, comp=True)
blqq3.fill_from_sph(sph3)
lam3, u3 = blqq3.get_eig(herm=False)


l = 8


blqq1.plot_slice(2, 0)
plt.title('cif -> cor -> blqq')

blqq2.plot_slice(2, 0)
plt.title('cif -> sph -> blqq')

blqq3.plot_slice(2, 0)
plt.title('cif -> ivol -> sph -> blqq')



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







