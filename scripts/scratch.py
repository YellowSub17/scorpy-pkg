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
cif.scat_sph[:,-1] *= 2
# cif.scat_sph[:,-1] *= np.random.random(len(cif.scat_sph[:,-1]))
# cif.scat_sph[:,-1] = np.abs(cif.scat_sph[:,-1])**2


# SET UP TARGET HARMONICS
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif)
sphv_targ.plot_slice(0,qq, title='Target')

# SET UP MASK
sphv_mask = sphv_targ.copy()
sphv_mask.make_mask()
sphv_mask.plot_slice(0,qq, title='Mask')



iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)






# SET UP ALGORITHM
a_sphv = scorpy.AlgoHandler(blqq_data, sphv_mask, sphv_start=True)
a_iqlm = scorpy.AlgoHandler(blqq_data, sphv_mask, sphv_start=False)

for i in range(5):
    print(i)
    a_iqlm.ER_iqlm()
    a_sphv.ER_sphv()
    # if i%1==0:
        # fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
        # a.sphv_add.plot_slice(0, qq, fig=fig, axes=axes[0])
        # a.sphv_b.plot_slice(0, qq, fig=fig, axes=axes[1])



plt.show()


















