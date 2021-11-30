#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





# Parameters
nq= 200
ntheta = 180
nphi = 360
nl = 90
qmax = 89


tag = 'targ_fcc_supp_ccc'

targ_cif_fname = 'fcc-sf.cif'
supp_cif_fname = 'ccc-sf.cif'



# Make directory to save vols
os.mkdir(f'{scorpy.DATADIR}/algo/{tag}')


# Generate Target
cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{targ_cif_fname}', qmax = qmax)
sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_targ.fill_from_cif(cif_targ)
sphv_targ.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')

# Generate Support 
cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{supp_cif_fname}', qmax = qmax)
sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_supp.fill_from_cif(cif_supp)
sphv_supp.make_mask()
sphv_supp.save(f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')



# Generate Data
iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
iqlm_targ.fill_from_sphv(sphv_targ)
sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
sphv_harmed.fill_from_iqlm(iqlm_targ)
blqq_data = scorpy.BlqqVol(nq, nl, qmax)
blqq_data.fill_from_iqlm(iqlm_targ)
blqq_data.save(f'{scorpy.DATADIR}/algo/{tag}/blqq_{tag}_data.dbin')











