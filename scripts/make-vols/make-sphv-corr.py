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


#open the spherical volume to correlate
sphv = scorpy.SphericalVol(path = f'{__DATADIR}/dbins/sphharm_sphv2')



# initiailize correlation volume
corr = scorpy.CorrelationVol(sphv.nq, sphv.nphi, sphv.qmax)

#mesh grid of phi and theta
pp, tt = np.meshgrid(sphv.phipts, sphv.thetapts)


t1 = time.time()
#for every pair of q1 and q2 shells...
for q1_ind in range(0, sphv.nq):
    q1_slice = sphv.vol[q1_ind, ...]
    for q2_ind in range(q1_ind, sphv.nq):
    # for q2_ind in range(0, sphv.nq):

        q2_slice = sphv.vol[q2_ind, ...]



        #for every orientation of shell
        for theta_ind in range(0, sphv.ntheta):
            print(q1_ind, q2_ind, theta_ind)
            for phi_ind in range(0, sphv.nphi):

                #change the orienation of shell
                pp_rolled = np.roll(pp, (theta_ind, phi_ind), (0, 1))
                tt_rolled = np.roll(tt, (theta_ind, phi_ind), (0, 1))

                #find the angle between unorientated and new orientation
                angle_between_flat = list(map(angle_between_sph, tt.flatten(), tt_rolled.flatten(), pp.flatten(), pp_rolled.flatten()))
                ite = np.ones(len(angle_between_flat))
                #find the index of psi, the angle between orientated shells
                angle_between_ind = list(map(index_x, angle_between_flat, -1 * ite, ite, sphv.nphi * ite, ite))

                #reshape the flattens array (flat arrays work well with map() )
                angle_between_rolled = np.array(angle_between_ind).reshape(sphv.ntheta, sphv.nphi)

                
                # II = q1_slice * np.roll(q2_slice, (theta_ind, phi_ind), (0, 1)) #* np.sin(tt_rolled) * np.sin(tt)

                # for angle_ind, II_val in zip(angle_between_rolled.flatten(), II.flatten()):
                    # corr.vol[q1_ind, q2_ind, angle_ind] += II_val

                #correlate the intensities, where q2 is oritented
                II1 = q1_slice * np.roll(q2_slice, (theta_ind, phi_ind), (0, 1)) #* np.sin(tt_rolled) * np.sin(tt)
                II2 = q2_slice * np.roll(q1_slice, (theta_ind, phi_ind), (0, 1)) #* np.sin(tt_rolled) * np.sin(tt)

                #for every pair of psi index and inntensity values, add them to the correlation volume

                if q1_ind == q2_ind:
                    for angle_ind, II_val in zip(angle_between_rolled.flatten(), II1.flatten()):
                        corr.vol[q1_ind, q2_ind, angle_ind] += II_val

                else:
                    for angle_ind, II_val in zip(angle_between_rolled.flatten(), II1.flatten()):
                        corr.vol[q1_ind, q2_ind, angle_ind] += II_val

                    for angle_ind, II_val in zip(angle_between_rolled.flatten(), II2.flatten()):
                        corr.vol[q2_ind, q1_ind, angle_ind] += II_val



print(time.time() - t1)



# corr.save(f'{__DATADIR}/dbins/sphharm_qcor2.dbin')
