import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
plt.close('all')







# Parameters
nq= 150
# ntheta = 180
# nphi = 360
# nl = 90

ntheta = 90
nphi = 180
nl = 45
qmax = 108

qq = 98

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
sphv_targ.vol = 6*sphv_targ.vol #+ np.random.random(sphv_targ.vol.shape)
# sphv_targ.plot_slice(0,qq, title='Target')


iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)

# SET UP BLQQ
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)




# SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_mask, iter_obj='sphv', lossy_sphv=False, lossy_iqlm=False)




sphv1 = a.sphv_iter.copy()
a.k_constraint_sphv()
sphv2 = a.sphv_iter.copy()
a.k_constraint_sphv()
sphv3 = a.sphv_iter.copy()
a.k_constraint_sphv()
sphv4 = a.sphv_iter.copy()

a.k_constraint_sphv()
sphv5 = a.sphv_iter.copy()
a.k_constraint_sphv()
sphv6 = a.sphv_iter.copy()


for i, s in enumerate([sphv1, sphv2, sphv3, sphv4, sphv5, sphv6]):
    s.plot_slice(0, qq, title=f'sphv{i+1}')




# t = time.time()
# for i in range(16):
    # print(i, end='\r')

    # a.ER()
 #    if i in [0,1,2,3,4] or i%5==0:
        # # a.sphv_iter.plot_slice(0, qq, title=f'{i}')
        # a.sphv_diff.plot_slice(0, qq, title=f'{i}')
        # a.sphvp.plot_slice(0, qq, title=f'{i}')
        # # a.sphv_add.plot_slice(0, qq, title=f'{i}')


# tf = time.time()-t

# print('')
# print(f'time: {tf}')


plt.show()


















