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




corr1 = scorpy.CorrelationVol(path="../data/dbins/1al1_sph_qcor")
corr2 = scorpy.CorrelationVol(path="../data/dbins/1al1_binned_sph_qcor")
corr3 = scorpy.CorrelationVol(path="../data/dbins/1al1_binned2_sph_qcor")


corr1.plot_sumax()
plt.title('corr before bin')

corr2.plot_sumax()
plt.title('corr after bin')

corr3.plot_sumax()
plt.title('corr half bin')






blqq1 = scorpy.BlqqVol(corr1.nq, 57, corr1.qmax)
blqq1.fill_from_corr(corr1)

blqq2 = scorpy.BlqqVol(corr2.nq, 57, corr2.qmax)
blqq2.fill_from_corr(corr2)

blqq3 = scorpy.BlqqVol(corr3.nq, 57, corr3.qmax)
blqq3.fill_from_corr(corr3)

blqq1.plot_slice(axis=2, index=14)
plt.title('blqq before bin')

blqq2.plot_slice(axis=2, index=14)
plt.title('blqq after bin')

blqq3.plot_slice(axis=2, index=14)
plt.title('blqq half bin')






# blqq3 = blqq2.copy()
# blqq3.vol -= blqq1.vol

# blqq3.plot_slice(axis=2, index=14)
# plt.title('diff')

plt.show()





















