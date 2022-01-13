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


figsize=(6,3.5)
dpi=125



# # # # ## Ps idempo test
# a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

# op = a.Ps


# fig, axes = plt.subplots(1,3, sharex=True, sharey=True, figsize=figsize, dpi=dpi)

# plt.tight_layout()

# plot_args = {'fig':fig,
            # 'xlabel': '$\\phi$ [rad]',}
# sphv1 = a.sphv_iter.copy()
# sphv1.plot_slice(0,qq, axes=axes[0], ylabel='$\\theta$ [rad]', title='$S_n(q=0.1, \\theta, \\phi)$', **plot_args)


# a.sphv_supp.plot_slice(0,qq, axes=axes[1], title='Bragg Mask', **plot_args)

# op()
# sphv2 = a.sphv_iter.copy()
# sphv2.plot_slice(0,qq, axes=axes[2],title='$P_B[S_n]$',  **plot_args)

# fig.subplots_adjust(
    # top=0.926,
    # bottom=0.142,
    # left=0.098,
    # right=0.937,
    # hspace=0.2,
    # wspace=0.245)





# ## Pm idempo test
# a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

# op = a.Pm


# fig, axes = plt.subplots(1,3, sharex=True, sharey=True, figsize=figsize, dpi=dpi)


# plt.tight_layout()

# plot_args = {'fig':fig,
             # 'xlabel': '$\\phi$ [rad]',}

# sphv1 = a.sphv_iter.copy()
# sphv1.plot_slice(0,qq, axes=axes[0], ylabel='$\\theta$ [rad]', title='$S_n(q=0.1, \\theta, \\phi)$', **plot_args)


# op()
# sphv1 = a.sphv_iter.copy()
# sphv1.plot_slice(0,qq, axes=axes[1],title='$P_K[S_n]$',  **plot_args)


# op()
# sphv2 = a.sphv_iter.copy()
# sphv2.plot_slice(0,qq, axes=axes[2],title='$P_K^2[S_n]$',  **plot_args)

# fig.subplots_adjust(
    # top=0.926,
    # bottom=0.142,
    # left=0.098,
    # right=0.937,
    # hspace=0.2,
    # wspace=0.245)





# ####### # # ## Pm solved test
# a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

# op = a.Pm

# a.sphv_iter = sphv_targ.copy()


# fig, axes = plt.subplots(1,3, sharex=True, sharey=True, figsize=figsize, dpi=dpi)

# plt.tight_layout()

# plot_args = {'fig':fig,
             # 'xlabel': '$\\phi$ [rad]',}

# sphv1 = a.sphv_iter.copy()
# sphv1.plot_slice(0,qq, axes=axes[0], ylabel='$\\theta$ [rad]', title='$S_t(q=0.1, \\theta, \\phi)$', **plot_args)


# op()
# sphv2 = a.sphv_iter.copy()
# sphv2.plot_slice(0,qq, axes=axes[1],title='$P_K[S_t]$',  **plot_args)


# # op()
# sphv3 = sphv2.copy()
# sphv3.vol -= sphv1.vol
# sphv3.plot_slice(0,qq, axes=axes[2],title='Difference',  **plot_args)

# fig.subplots_adjust(
    # top=0.926,
    # bottom=0.142,
    # left=0.098,
    # right=0.937,
    # hspace=0.2,
    # wspace=0.245)






plt.show()




















