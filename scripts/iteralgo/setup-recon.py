#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# # # Parameters
nq= 50
ntheta = 90
nphi = 180
nl = 45
npsi = 360*32
qmax = 0.5

rcond = 0.1

from_corr = False



tag = 'p1-inten-r0-from-blqq-d100'

targ_cif_fname = 'p1-inten-r0-sf.cif'
supp_cif_fname = 'p1-inten-r0-sf.cif'




# # # Generate Target
cif_targ = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/{targ_cif_fname}', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)


# # # Generate Support 
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{supp_cif_fname}', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()




# # # Generate Data (from corr)
if from_corr:
    corr_data = scorpy.CorrelationVol(nq, npsi, qmax)
    corr_data.fill_from_cif(cif_targ)

    blqq_data = scorpy.BlqqVol(nq, nl, qmax)
    blqq_data.fill_from_corr(corr_data, rcond=0.1)



    corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
    corr_calc.fill_from_blqq(blqq_data)


# # # Generate Data (from harm)
else:
    iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
    iqlm_targ.fill_from_sphv(sphv_targ)
    sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
    sphv_harmed.fill_from_iqlm(iqlm_targ)

    blqq_data = scorpy.BlqqVol(nq, nl, qmax)
    blqq_data.fill_from_iqlm(iqlm_targ)

    blqq_data.vol[:,:,41:] *=0

    blqq_data.vol *=1/100


    corr_calc = scorpy.CorrelationVol(nq, npsi, qmax)
    corr_calc.fill_from_blqq(blqq_data)





# Make directory to save vols
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}')

sphv_targ.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
cif_targ.save(f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif')
sphv_supp.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

blqq_data.save(f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')

# corr_calc.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_calc.dbin')
# if from_corr:
    # corr_data.save(f'{scorpy.DATADIR}/algo/{tag}/qcor_{tag}_data.dbin')









