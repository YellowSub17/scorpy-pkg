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

for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]:
    for seed in range(10):
        print('seed:', seed, 'n:', n)
        corr_seed = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/espk/ensemble_n{n}_{seed}')

        corr_sum.vol += corr_seed.vol


corr_fj = scorpy.CorrelationVol(path=f'{__DATADIR}/dbins/xtal/1vds_fj_qcor.dbin')
# corr_fj.sub_t_mean()
# corr_sum.sub_t_mean()


corr_sum.plot_q1q2()
plt.title('2D esp q1=q2')
corr_fj.plot_q1q2()
plt.title('3D esp q1=q2')


plt.figure()
plt.imshow(corr_sum.get_xy()[:,10:-10], origin='lower', extent=[corr_sum.psipts[10], corr_sum.psipts[-10], 0, corr_sum.qmax])
plt.title('2D esp q1=q2 (cropped 10)')


corr_sum.plot_q1q2(log=True)
plt.title('2D esp q1=q2 (log)')
corr_fj.plot_q1q2(log=True)
plt.title('3D esp q1=q2 (log)')


qsum1 = corr_sum.vol.sum(axis=1).sum(axis=1)
qsum2 = corr_fj.vol.sum(axis=1).sum(axis=1)

plt.figure()
plt.title('Sum Correlation(q)')
plt.plot(corr_sum.qpts, qsum1 / qsum1.max(), label='2D esp')
plt.plot(corr_sum.qpts, qsum2 / qsum2.max(), label='3D esp')
plt.legend()

lhs = 10
rhs = -10

psum1 = corr_sum.vol.sum(axis=0).sum(axis=0)[lhs:rhs]
psum2 = corr_fj.vol.sum(axis=0).sum(axis=0)[lhs:rhs]

psi = corr_sum.psipts[lhs:rhs]

plt.figure()
plt.title('Sum Correlation(psi)')
plt.plot(psi, psum1 / psum1.max(), label='2D esp')
plt.plot(psi, psum2 / psum2.max(), label='3D esp')
# plt.plot(psi, (psum1*psum2.max()) / (psum2*psum1.max()), label='ratio')
plt.legend()


cif = scorpy.CifData(f'{__DATADIR}/xtal/1vds_fj-sf.cif')
geo = scorpy.ExpGeom(f'{__DATADIR}/geoms/agipd_2304_vj_opt_v3.geom')
pk = scorpy.PeakData(f'{__DATADIR}/espk/n1024/peaks_1024_9.txt', geo, cxi_flag=False)


plt.figure()
plt.title('3D esp Intensity Histogram')
plt.hist(cif.scat_sph[:, 0], bins=100, weights=cif.scat_sph[:, -1], color='orange')

plt.figure()
plt.title('2D esp Intensity Histogram')
plt.hist(pk.scat_pol[:, 0], bins=100, weights=pk.scat_pol[:, -1])


# plt.figure()
# plt.title('2D esp Peaks')
# geo.plot_panels()
# pk.split_frames()[0].plot_peaks()




plt.figure()
plt.hist(cif.scat_bragg[:,-1], bins=100)
plt.title('cif inten dist')
plt.xlabel('Intensity')
plt.ylabel('frequency')

plt.figure()
plt.hist(pk.scat_pol[:,-1], bins=100)
plt.title('pk inten dist')
plt.xlabel('Intensity')
plt.ylabel('frequency')


plt.show()
