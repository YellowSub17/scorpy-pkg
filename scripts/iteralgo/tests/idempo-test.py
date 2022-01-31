import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')







# Parameters
nq= 200
ntheta = 10
nphi = 20
nl = 5

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




# # # SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

# a.sphv_iter = sphv_targ.copy()



# a.Ps()

op = a.Pm





fig, axes = plt.subplots(1,3, sharex=True, sharey=True)

plot_args = {'fig':fig,
             'xlabel': '$\\phi$ [rad]',
             'ylabel': '$\\theta$ [rad]',}

sphv1 = a.sphv_iter.copy()
sphv1.plot_slice(0,qq, axes=axes[0], title='$S_n(q=0.1, \\theta, \\phi)$', **plot_args)


op()
sphv2 = a.sphv_iter.copy()
sphv2.plot_slice(0,qq, axes=axes[1],title='$P[S_n(q=0.1, \\theta, \\phi)]$',  **plot_args)

op()
sphv2 = a.sphv_iter.copy()
sphv2.plot_slice(0,qq, axes=axes[2],title='$P^2[S_n(q=0.1, \\theta, \\phi)]$',  **plot_args)








plt.show()




















