import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')
import timeit


np.random.seed(0)





# Parameters
nq= 200
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



sphv_init = sphv_harmed.copy()
sphv_init.vol = np.random.random(sphv_harmed.vol.shape)
# # # SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

a.sphv_iter = sphv_init.copy()



fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
a.sphv_iter.plot_slice(0,qq, fig=fig, axes=axes[0])
# a.Pm_debug()
t1 = timeit.timeit('a.Pm_debug()', globals=globals(), number=1)
a.sphv_iter.plot_slice(0,qq, fig=fig, axes=axes[1])


a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)
a.sphv_iter = sphv_init.copy()

fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
a.sphv_iter.plot_slice(0,qq, fig=fig, axes=axes[0])
# a.Pm()
t2 = timeit.timeit('a.Pm()', globals=globals(), number=1)
a.sphv_iter.plot_slice(0,qq, fig=fig, axes=axes[1])




plt.show()


