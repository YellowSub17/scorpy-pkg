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
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)



# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_mask)

for i in range(5):
    print(i)
    a.ER()
    a.sphv_add.plot_slice(0, qq)



plt.show()


















