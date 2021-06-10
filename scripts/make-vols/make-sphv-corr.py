#!/usr/bin/env python3
'''
make-sphv-corr.py

Make correlation vol objects from spherical vol
'''

import matplotlib.pyplot as plt
import scorpy
from scorpy import __DATADIR
from scorpy.utils import angle_between_sph, index_x
import numpy as np
import time
np.random.seed(0)


sphv = scorpy.SphericalVol(path = f'{__DATADIR}/dbins/sphharm_sphv')


corr = scorpy.CorrelationVol(sphv.nq, sphv.nphi, sphv.qmax)


pp, tt = np.meshgrid(sphv.phipts, sphv.thetapts)

for q1_ind in range(0, sphv.nq):
    q1_slice = sphv.vol[q1_ind, ...]

    for q2_ind in range(0, sphv.nq):
        q2_slice = sphv.vol[q2_ind, ...]

        print(q1_ind, q2_ind)

        for theta_ind in range(0, sphv.ntheta):

            for phi_ind in range(0, sphv.nphi):


                pp_rolled = np.roll(pp, (theta_ind, phi_ind), (0, 1))
                tt_rolled = np.roll(tt, (theta_ind, phi_ind), (0, 1))

                angle_between_flat = list(map(angle_between_sph, tt.flatten(), tt_rolled.flatten(), pp.flatten(), pp_rolled.flatten()))
                ite = np.ones(len(angle_between_flat))
                angle_between_ind = list(map(index_x, angle_between_flat, -1 * ite, ite, sphv.nphi * ite, ite))

                angle_between_rolled = np.array(angle_between_ind).reshape(sphv.ntheta, sphv.nphi)

                II = q1_slice * np.roll(q2_slice, (theta_ind, phi_ind), (0, 1)) #* np.sin(tt_rolled) * np.sin(tt)

                for angle_ind, II_val in zip(angle_between_rolled.flatten(), II.flatten()):
                    corr.vol[q1_ind, q2_ind, angle_ind] += II_val
                    # if q1_ind != q2_ind:
                        # corr.vol[q2_ind, q1_ind, angle_ind] += II_val





plt.figure()
plt.plot(corr.psipts, corr.vol[1,8,:])
plt.title('q1=1, q2=8')
plt.figure()
plt.plot(corr.psipts, corr.vol[8,1,:])
plt.title('q1=8, q2=1')
plt.show()



corr.save(f'{__DATADIR}/dbins/sphharm_qcor.dbin')
