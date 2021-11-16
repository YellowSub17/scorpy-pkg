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



# # # SET UP ALGORITHM
a = scorpy.AlgoHandler(blqq_data, sphv_supp, lossy_sphv=True, lossy_iqlm=True, rcond=1e-15)

# a.ER()

# a.sphv_d.vol = sphv_targ.vol - a.sphv_iter.vol
# d1 = a.sphv_d.copy()

# for i in range(10):
    # print(i)
    # a.ER()

# a.sphv_d.vol = sphv_targ.vol - a.sphv_iter.vol
# d2 = a.sphv_d.copy()




# for x in range(10,201,10):
    # s1 = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/sphv_iter_HIO_{x}')
    # d1 = sphv_targ.copy()
    # d1.vol -=s1.vol

    # if x % 50 == 0:
        # s1.plot_slice(0, qq)
        # d1.plot_slice(0, qq)

    # print(d1.vol[a.supp_loc].mean())






fig, axes = plt.subplots(4,4, sharex=True, sharey=True)

errs = []
for i in range(0, 16):
    s = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/sphv_iter_HIO_200_ER_{i*10}')
    d = sphv_targ.copy()
    d.vol -=s.vol
    print(d.vol[a.supp_loc].mean())
    errs.append(d.vol[a.supp_loc].mean())

    s.plot_slice(0, qq, title=f'{i}', fig=fig, axes=axes.flatten()[i])

plt.figure()
plt.plot(list(range(0, 16)), errs)
plt.xlabel('iter #')
plt.ylabel('mean difference between target and iter')







# sphv_init = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/HIO/sphv_iter_HIO_200')
# a.sphv_iter = sphv_init.copy()

# print(time.asctime())

# for i in range(0, 200):
    # print(i, end='\r')

    # if i%10==0:
        # a.sphv_iter.save(f'{scorpy.DATADIR}/algo/sphv_iter_HIO_200_ER_{i}')
    # a.ER()

# a.sphv_iter.save(f'{scorpy.DATADIR}/algo/sphv_iter_HIO_200_ER_200')

# print(time.asctime())








plt.show()













                      
