#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters
nq= 100
ntheta = 180
nphi = 360
nl = 90
qmax = 89


supp_cif_fname = 'ccc-sf.cif'
targ_cif_fname = 'fcc-sf.cif'

tag = "HIO_ER_1"


# Make directory to save vols
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}/')

# SET UP MASK DATA
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{supp_cif_fname}', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()
sphv_supp.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')


# SET UP TARGET DATA
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{targ_cif_fname}', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
sphv_targ.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')



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
a.sphv_iter = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo.bkup/HIO_ER_fcc_b/sphv_HIO_ER_fcc_b_0.dbin')


print(time.asctime())

a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_init.dbin')

count =0
for set_num in range(1):

    for op, op_str in zip([a.HIO, a.ER], ['HIO', 'ER']):

        print(f'Set: {set_num}\tOp: {op_str}')
        for iter_num in range(200):

            print('                      ',end='\r')
            print(f'{iter_num}', end='\r')

            if iter_num %10==0:
                a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_{count}.dbin')

            _, _, err = op()
            count +=1

            errs_file = open(f'{scorpy.DATADIR}/algo/{tag}/errs_{tag}.log', 'a')
            errs_file.write(f'{err},\t\t#{tag}_{count}\n')
            errs_file.close()



print(time.asctime())
a.sphv_iter.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_{count}.dbin')




