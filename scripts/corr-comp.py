#!/usr/bin/env python3
'''
corr-comp.py

Compare various correlation vols
'''



import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np






corr1 = scorpy.CorrelationVol(path="../data/dbins/1al1_sph_qcor")
corr2 = scorpy.CorrelationVol(path="../data/dbins/1al1_binned_sph_qcor")
corr3 = scorpy.CorrelationVol(path="../data/dbins/1al1_binned_half_sph_qcor")
corr4 = scorpy.CorrelationVol(path="../data/dbins/1al1_binned_double_sph_qcor")


blqq1 = scorpy.BlqqVol(corr1.nq, 27, corr1.qmax)
blqq1.fill_from_corr(corr1)

blqq2 = scorpy.BlqqVol(corr2.nq, 27, corr2.qmax)
blqq2.fill_from_corr(corr2)

blqq3 = scorpy.BlqqVol(corr3.nq, 27, corr3.qmax)
blqq3.fill_from_corr(corr3)

blqq4 = scorpy.BlqqVol(corr4.nq, 27, corr4.qmax)
blqq4.fill_from_corr(corr4)



lam1, u1 = blqq1.get_eig(herm=True)
lam2, u2 = blqq2.get_eig(herm=True)
lam3, u3 = blqq3.get_eig(herm=True)
lam4, u4 = blqq4.get_eig(herm=True)




corr1.plot_sumax()
plt.title('corr before bin')

corr2.plot_sumax()
plt.title('corr after bin')

corr3.plot_sumax()
plt.title('corr half bin')

corr4.plot_sumax()
plt.title('corr double bin')



blqq1.plot_slice(axis=2, index=14)
plt.title('blqq before bin')

blqq2.plot_slice(axis=2, index=14)
plt.title('blqq after bin')

blqq3.plot_slice(axis=2, index=14)
plt.title('blqq half bin')

blqq4.plot_slice(axis=2, index=14)
plt.title('blqq double bin')



plt.figure()
plt.imshow(lam1)
plt.title('lam before bin')
plt.colorbar()

plt.figure()
plt.imshow(lam2)
plt.title('lam after bin')
plt.colorbar()

plt.figure()
plt.imshow(lam3)
plt.title('lam half bin')
plt.colorbar()

plt.figure()
plt.imshow(lam4)
plt.title('lam double bin')
plt.colorbar()


plt.show()





















