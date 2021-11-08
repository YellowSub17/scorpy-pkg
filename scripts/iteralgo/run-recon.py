#!/usr/bin/env python3
'''
solved-test.py

replaces the initial spherical volume object with the target solution,
and ensures the same values are returned after one iteration.
'''
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')


np.random.seed(0)







# Parameters
nq= 200
ntheta = 180
nphi = 360
nl = 90


qmax = 89

qq = 72



# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()
sphv_supp.plot_slice(0, qq, title='support')
loc = np.where(sphv_supp.vol>0)
q_loc1 = np.unique(loc[0])


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/bcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
loc = np.where(sphv_targ.vol>0)
q_loc2 = np.unique(loc[0])

# add noise
# sphv_targ.vol *= 100
# sphv_targ.vol[loc] += 2*np.random.random(sphv_targ.vol.shape)[loc]

sphv_targ.plot_slice(0, qq, title='target')


# get harmonic coefficients
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# get harmonic filtered bragg spots
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1e-3)


sphv_init = a.sphv_iter.copy()


print(time.asctime())
# for each algorithm scheme
for op in [a.ER, a.DM, a.RAAR, a.HIO, a.SF, a.ASR, a.HPR]:
# for op in [a.ER, a.DM]:
    print(op, '\n')

    a.sphv_iter = sphv_init.copy()

    fig, axes = plt.subplots(3,3, sharex=True, sharey=True)
    plt.suptitle(op)

    for i in range(9):
        print(i, end='\r')


        op()

        a.sphv_iter.plot_slice(0, qq, title=f'{i}', fig=fig,axes=axes.flatten()[i])

    print()


print(time.asctime())




plt.show()















