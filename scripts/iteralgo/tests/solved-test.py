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
nq= 201
ntheta = 180
nphi = 360
nl = 90

qmax = 89





# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/ccc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

sphv_targ.vol *= np.random.random(sphv_targ.vol.shape)

loc = np.where(sphv_targ.vol>0)
q_inds = np.unique(loc[0])
qq = q_inds[-4]



# get harmonic coefficients
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# get harmonic filtered bragg spots
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# # # SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)






# for each algorithm scheme
for op in [a.ER, a.DM, a.RAAR, a.HIO, a.SF, a.ASR, a.HPR]:

    # place algorithm in "solved" state
    a.sphv_iter = sphv_targ.copy()
    print(op)

    fig, axes = plt.subplots(3,2)
    plt.suptitle(op)

    a.sphv_iter.plot_slice(0, qq, title='initial', fig=fig, axes=axes[0,0])
    a.sphv_supp.plot_slice(0, qq, title='supp', fig=fig, axes=axes[0,1])

    in1, out1, err = op()
    print(err)
    a.sphv_iter.plot_slice(0, qq, title='iter1', fig=fig, axes=axes[1,0])

    out1.vol -= in1.vol
    out1.plot_slice(0, qq, title='diff1', fig=fig, axes=axes[1,1])


    in2, out2, err = op()
    print(err)
    a.sphv_iter.plot_slice(0, qq, title='iter2', fig=fig, axes=axes[2,0])

    out2.vol -= in2.vol
    out2.plot_slice(0, qq, title='diff2', fig=fig, axes=axes[2,1])
    print()

plt.show()















