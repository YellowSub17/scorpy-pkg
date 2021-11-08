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

qq = 89

# SET UP MASK DATA
cif_mask = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif_mask)
sphv_mask.make_mask()
# sphv_mask.plot_slice(0,qq, title='Mask')


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)

# sphv_targ.vol = np.random.random(sphv_targ.vol.shape)
# sphv_targ.vol = 6*sphv_targ.vol #+ np.random.random(sphv_targ.vol.shape)
# sphv_targ.plot_slice(0,qq, title='Target')


iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_mask,
                       lossy_sphv=True, lossy_iqlm=True, rcond=1, inc_odds=False)

# a.Ps()

op = a.Pm
# a.sphv_iter = sphv_targ




#CHeck -1 factor, -1^L, inc-odds
fig, axes = plt.subplots(2,3, sharex=True, sharey=True)

sphv1 = a.sphv_iter.copy()
sphv1.plot_slice(0,qq, title='initial', fig=fig, axes=axes[0,0])
print(1)

op()
sphv2 = a.sphv_iter.copy()
sphv2.plot_slice(0,qq, title='iter1', fig=fig, axes=axes[0,1])

print(2)
op()
sphv3 = a.sphv_iter.copy()
sphv3.plot_slice(0,qq, title='iter2', fig=fig, axes=axes[0,2])

print(3)
op()
sphv4 = a.sphv_iter.copy()
sphv4.plot_slice(0,qq, title='iter3', fig=fig, axes=axes[1,0])

print(4)
op()
sphv5 = a.sphv_iter.copy()
sphv5.plot_slice(0,qq, title='iter4', fig=fig, axes=axes[1,1])

print(5)
op()
sphv6 = a.sphv_iter.copy()
sphv6.plot_slice(0,qq, title='iter5', fig=fig, axes=axes[1,2])


s21 = sphv2.copy()
s21.vol -= sphv1.vol

s32 = sphv3.copy()
s32.vol -=sphv2.vol

s43 = sphv4.copy()
s43.vol -=sphv3.vol

s54 = sphv5.copy()
s54.vol -=sphv4.vol


fig, axes = plt.subplots(2,2, sharex=True, sharey=True)
plt.suptitle('Differences')
s21.plot_slice(0,qq, title='iter1 - initial', fig=fig, axes=axes[0,0])
s32.plot_slice(0,qq, title='iter2 - iter1', fig=fig, axes=axes[0,1])
s43.plot_slice(0,qq, title='iter3 - iter2', fig=fig, axes=axes[1,0])
s54.plot_slice(0,qq, title='iter4 - iter3', fig=fig, axes=axes[1,1])




plt.show()




















