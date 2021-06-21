#!/usr/bin/env python3
'''
espk-cif-comp.py

Compare the correlation volumes from simulated ensemble peaks and cif data

'''
import numpy as np
import scorpy
from scorpy.env import __DATADIR
import matplotlib.pyplot as plt
import time

plt.close('all')


corr_sum = scorpy.CorrelationVol(100, 180, 1.4)


for seed in range(10):
    print('seed:', seed)
    corr_seed = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/ensemble_peaks/ensemble_n1024_{seed}')

    corr_sum.vol += corr_seed.vol


corr_fj = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/1vds_fj_qcor.dbin')
# corr_fj.sub_t_mean()
# corr_sum.sub_t_mean()


corr_sum.plot_q1q2()
plt.title('2D esp q1=q2')

corr_fj.plot_q1q2()
plt.title('3D esp q1=q2')

corr_sum.plot_q1q2(log=True)
plt.title('2D esp q1=q2 (log)')


qsum1 = corr_sum.vol.sum(axis=1).sum(axis=1)
qsum2 = corr_fj.vol.sum(axis=1).sum(axis=1)
qsum3 = corr_fj.vol.sum(axis=1).sum(axis=1) / corr_fj.qpts

plt.figure()
plt.title('Sum Correlation(q)')
plt.plot(corr_sum.qpts, qsum1 / qsum1.max(), label='2D esp')
plt.plot(corr_sum.qpts, qsum2 / qsum2.max(), label='3D esp')
plt.plot(corr_sum.qpts, qsum3 / qsum3.max(), label='3D esp/q')
plt.legend()


psum1 = corr_sum.vol.sum(axis=0).sum(axis=0)
psum2 = corr_fj.vol.sum(axis=0).sum(axis=0)

plt.figure()
plt.title('Sum Correlation(psi)')
plt.plot(corr_sum.psipts, psum1 / psum1.max(), label='2D esp')
plt.plot(corr_sum.psipts, psum2 / psum2.max(), label='3D esp')
plt.legend()


cif = scorpy.CifData(f'{__DATADIR}/xtal/1vds_fj-sf.cif')
geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')
pk = scorpy.PeakData(f'{__DATADIR}/ensemble_peaks/n1024/peaks_1024_9.txt', geo, cxi_flag=False)


plt.figure()
plt.title('3D esp Intensity Histogram')
plt.hist(cif.scat_sph[:, 0], bins=200, weights=cif.scat_sph[:, -1], color='orange')

plt.figure()
plt.title('2D esp Intensity Histogram')
plt.hist(pk.scat_pol[:, 0], bins=200, weights=pk.scat_pol[:, -1])


plt.figure()
plt.title('2D esp Peaks')
geo.plot_panels()
pk.split_frames()[0].plot_peaks()


plt.figure()
q = corr_fj.get_xy()[:, -2] / corr_fj.qpts
qy = corr_sum.get_xy()[:, -2]


ratio = q / qy


plt.plot(ratio)

plt.show()
