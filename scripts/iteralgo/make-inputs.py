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


tag = 'fcc'


for tag in ['fcc', 'ccc', 'fcc-rand', 'ccc-rand']:
# Make directory to save vols

# SET UP MASK DATA
    cif_supp = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{tag}-sf.cif', qmax = qmax)
    sphv_supp = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
    sphv_supp.fill_from_cif(cif_supp)
    sphv_supp.make_mask()
    sphv_supp.save(f'{scorpy.DATADIR}/algo/INPUTS/sphv_{tag}_supp.dbin')


# SET UP TARGET DATA
    cif_targ = scorpy.CifData(f'{scorpy.DATADIR}/cifs/{tag}-sf.cif', qmax = qmax)
    sphv_targ = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
    sphv_targ.fill_from_cif(cif_targ)
    sphv_targ.save(f'{scorpy.DATADIR}/algo/INPUTS/sphv_{tag}_targ.dbin')



# get harmonic coefficients
    iqlm_targ = scorpy.IqlmHandler(nq, nl, qmax)
    iqlm_targ.fill_from_sphv(sphv_targ)

# get harmonic filtered bragg spots
    sphv_harmed = scorpy.SphericalVol(nq, ntheta, nphi, qmax)
    sphv_harmed.fill_from_iqlm(iqlm_targ)

# SET UP BLQQ
    blqq_data = scorpy.BlqqVol(nq, nl, qmax)
    blqq_data.fill_from_iqlm(iqlm_targ)

    blqq_data.save(f'{scorpy.DATADIR}/algo/INPUTS/blqq_{tag}_targ.dbin')





