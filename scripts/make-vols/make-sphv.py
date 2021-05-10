#!/usr/bin/env python3
'''
make-sphv.py

Make Spherical vol objects.
'''

import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt


nq = 200
nangle = 360
gridtype = 'DH2'
extend = False


cif = scorpy.CifData('../data/xtal/1al1-sf.cif')
sphvol = scorpy.SphericalVol(
    256, nangle, qmax=cif.qmax, gridtype=gridtype, extend=extend)

sphvol.fill_from_cif(cif)
sphvol.save_dbin('../data/dbins/1al1_sphv')
