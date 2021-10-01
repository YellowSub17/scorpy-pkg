import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')


# Parameters
nq= 100
ntheta = 180
nphi = 360
nl = 90
qmax = 108

qq = 49

# SET UP DATA
cif = scorpy.CifData(f'{scorpy.DATADIR}/cifs/fcc-sf.cif', qmax = qmax)

# SET UP MASK
sphv_mask = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_mask.fill_from_cif(cif)
sphv_mask.make_mask()
sphv_mask.plot_slice(0,qq)

# SET UP TARGET HARMONICS
sphv_targ = sphv_mask.copy()
sphv_targ.vol *= np.random.random(sphv_targ.vol.shape)
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# i = scorpy.IqlmHandler(nq, nl, qmax)
# i.vals = np.random.random(i.vals.shape)
# i.vals = np.ones(i.vals.shape)


# s = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
# s.fill_from_iqlm(i)

# s.plot_slice(0, qq)


# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_mask)

for i in range(10):
    print(i)
    a.ER()
    if i%2==0:
        a.sphv_add.plot_slice(0, qq)



plt.show()


















