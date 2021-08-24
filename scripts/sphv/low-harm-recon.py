#!/usr/bin/env/ python3
'''
low-harm-recon.py

compare various volumes (blqq, sphv, corr) of low spherical harmonics calculated in various methods
'''
import numpy as np
import scorpy
from scorpy import __DATADIR
from scorpy.utils import angle_between_sph, index_x
import matplotlib.pyplot as plt
plt.close('all')
np.random.seed(0)


nq = 10
ntheta = 18 * 2
nphi = 36 * 2
lmax = 8
qmax = 1





sphv = scorpy.SphericalVol(path=f'{__DATADIR}/low-harm/low-harm_sphv')



# BlqqVol from SphericalVol of singular harmonics
blqq1 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq1.fill_from_sphv(sphv)


# CorrelationVol from SphericalVol of single spherical harmonics
corr1 = scorpy.CorrelationVol(path=f'{__DATADIR}/low-harm/low-harm_qcor')



# BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
blqq2 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq2.fill_from_corr(corr1, inc_odds=False)


# CorrelationVol from BlqqVol from CorrelationVol from SphericalVol of single spherical harmonics
corr2 = scorpy.CorrelationVol(nq, nphi, qmax)
corr2.fill_from_blqq(blqq2, inc_odds=False)


# CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
corr3 = scorpy.CorrelationVol(nq, nphi, qmax)
corr3.fill_from_blqq(blqq1, inc_odds=False)

# BlqqVol from CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
blqq3 = scorpy.BlqqVol(nq, sphv.nl, qmax)
blqq3.fill_from_corr(corr3, inc_odds=False)

# CorrelationVol from BlqqVol from CorrelationVol from BlqqVol from SphericalVol of single spherical harmonics
corr4 = scorpy.CorrelationVol(nq, nphi, qmax)
corr4.fill_from_blqq(blqq3, inc_odds=False)


sphv.plot_slice(0, 4)
plt.title('sphv L=2 M=1')
plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-sphv21.png')

sphv.plot_slice(0, 9)
plt.title('sphv L=4 M=2')
plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-sphv42.png')

for i, corr in enumerate([corr1, corr2, corr3, corr4]):
    corr.plot_q1q2()
    plt.title(f'corr{i+1}')
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-corr{i+1}.png')



l = 0
for i, blqq in enumerate([blqq1, blqq2, blqq3 ]):
    blqq.plot_slice(2, l)
    plt.title(f'blqq{i+1}, l={l}')
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-blqq{i+1}l{l}.png')


l = 2
for i, blqq in enumerate([blqq1, blqq2, blqq3 ]):
    blqq.plot_slice(2, l)
    plt.title(f'blqq{i+1}, l={l}')
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-blqq{i+1}l{l}.png')

l = 4
for i, blqq in enumerate([blqq1, blqq2,  blqq3]):
    blqq.plot_slice(2, l)
    plt.title(f'blqq{i+1}, l={l}')
    plt.savefig(f'/home/pat/Documents/cloudstor/phd/latex/scorpy-script-reports/figs/low-harm-recon-blqq{i+1}l{l}.png')

plt.show()
