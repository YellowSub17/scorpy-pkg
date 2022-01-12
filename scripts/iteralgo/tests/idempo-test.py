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



a.Ps()

op = a.Pm




# fig, axes = plt.subplots(2,3, sharex=True, sharey=True)

sphv1 = a.sphv_iter.copy()
# sphv1.plot_slice(0,qq, title='initial', fig=fig, axes=axes[0,0])
sphv1.plot_slice(0,qq)



op()
sphv2 = a.sphv_iter.copy()
sphv2.plot_slice(0,qq)
# sphv2.plot_slice(0,qq, title='iter1', fig=fig, axes=axes[0,1])

op()
sphv2 = a.sphv_iter.copy()
sphv2.plot_slice(0,qq)






# print(2)
# op()
# sphv3 = a.sphv_iter.copy()
# sphv3.plot_slice(0,qq, title='iter2', fig=fig, axes=axes[0,2])


# print(3)
# op()
# sphv4 = a.sphv_iter.copy()
# sphv4.plot_slice(0,qq, title='iter3', fig=fig, axes=axes[1,0])

# print(4)
# op()
# sphv5 = a.sphv_iter.copy()
# sphv5.plot_slice(0,qq, title='iter4', fig=fig, axes=axes[1,1])

# print(5)
# op()
# sphv6 = a.sphv_iter.copy()
# sphv6.plot_slice(0,qq, title='iter5', fig=fig, axes=axes[1,2])


# s21 = sphv2.copy()
# s21.vol -= sphv1.vol

# s32 = sphv3.copy()
# s32.vol -=sphv2.vol

# s43 = sphv4.copy()
# s43.vol -=sphv3.vol

# s54 = sphv5.copy()
# s54.vol -=sphv4.vol


# fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
# plt.suptitle('Differences')
# s21.plot_slice(0,qq, title='iter1 - initial', fig=fig, axes=axes[0,0])
# s32.plot_slice(0,qq, title='iter2 - iter1', fig=fig, axes=axes[0,1])
# s43.plot_slice(0,qq, title='iter3 - iter2', fig=fig, axes=axes[1,0])
# s54.plot_slice(0,qq, title='iter4 - iter3', fig=fig, axes=axes[1,1])




plt.show()




















