#!/usr/bin/env python3
'''
blqq-comp.py

Calculate the blqq matrix with various methods and compare the results.
'''



import scorpy
import matplotlib.pyplot as plt
import numpy as np

from scorpy.utils import cosinesim


plt.close('all')

cor1 = scorpy.CorrelationVol(path='../data/dbins/1al1_qcor')

cor1.plot_q1q2(extent=None)
plt.title('Original Corr')
plt.ylabel('q1=q2')
plt.xlabel('theta')


cor1.plot_q1q2(extent=None)
plt.title('Original Corr')
plt.ylabel('q1=q2')
plt.xlabel('theta')


cif1 = scorpy.CifData('../data/xtal/1al1-sf.cif',qmax=cor1.qmax)

comp = False
nl = 67

blqq1 =scorpy.BlqqVol(cor1.nq, nl, cor1.qmax, comp=comp)

blqq1.fill_from_corr(cor1)

# cor2 = cor1.copy()
# cor2.vol *=0
# cor2.fill_from_blqq(blqq1)






i=180
plt.figure()
plt.subplot(121)
cor1.plot_slice(2,i,False,extent=None)
plt.title(i)

plt.subplot(122)
cor1.plot_slice(2,cor1.ntheta-1-i,False,extent=None)
plt.title(cor1.ntheta - 1-i)


# cor2.plot_q1q2()
# plt.title('Cor -> blqq -> Cor')
# plt.ylabel('q1=q2')
# plt.xlabel('theta')



# cor1.plot_q1q2()
# plt.title('Original Corr')
# plt.xlim(70,110)
# plt.ylim(0.03, 0.06)
# plt.ylabel('q1=q2')
# plt.xlabel('theta')

# cor2.plot_q1q2()
# plt.title('Cor -> blqq -> Cor')
# plt.xlim(70,110)
# plt.ylim(0.03, 0.06)
# plt.ylabel('q1=q2')
# plt.xlabel('theta')
plt.show()











