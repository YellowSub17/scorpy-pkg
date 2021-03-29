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

cor = scorpy.CorrelationVol(path='../data/dbins/1al1_qcor')
cor.force_sym()
# cor.sub_tmean()
# cor.convolve(std_z = 2)




cif = scorpy.CifData('../data/xtal/1al1-sf.cif',qmax=cor.qmax)

comp = False
nl = 17

blqq_base =scorpy.BlqqVol(cor.nq, nl, cor.qmax, comp=comp)
sphharm_base = scorpy.SphHarmHandler(cor.nq, nl, cor.qmax, comp=comp)




blqq1 = blqq_base.copy()
blqq1.fill_from_corr(cor)
lam1, u1 = blqq1.get_eig(herm=True)
lam1a, u1a = blqq1.get_eig(herm=False)


sph2 = sphharm_base.copy()
sph2.fill_from_cif(cif)
blqq2 = blqq_base.copy()
blqq2.fill_from_sph(sph2)
lam2, u2 = blqq2.get_eig(herm=True)
lam2a, u2a = blqq2.get_eig(herm=False)


blqq1.convolve()
blqq2.convolve()

print(f'Cosine Sim (1-2): {cosinesim(blqq1.vol, blqq2.vol)}\n')



cor.plot_q1q2()
ls = [0, 8, 10,16]
for l in ls:

    plt.figure()

    plt.subplot(121)
    blqq1.plot_slice(2, l, new_fig=False)
    plt.title(f'bl1: cif -> cor -> blqq (l={l})')

    plt.subplot(122)
    blqq2.plot_slice(2, l, new_fig=False)
    plt.title(f'bl2: cif -> sph -> blqq (l={l})')




lams = [lam1, lam2, lam1a, lam2a]
titles = [  'blqq1 lamda: cif -> cor -> blqq', 
            'blqq2 lamda: cif -> sph -> blqq',
            'blqq1 lamda_a: cif -> cor -> blqq',
            'blqq2 lamda_a: cif -> sph -> blqq',]

for lam, title in zip(lams, titles):
    plt.figure()
    plt.imshow(np.log10(np.abs(lam)+1), aspect='auto')
    plt.colorbar()
    plt.title(title)
    plt.xlabel('L')
    plt.ylabel('nq')

plt.show()







