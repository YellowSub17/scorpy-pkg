#!/usr/bin/env python3
'''
make-cif-corr.py

Make correlation vol objects from cif data.
'''

import matplotlib.pyplot as plt
import scorpy
from scorpy import __DATADIR
import numpy as np
import time
np.random.seed(0)


# MAKE CORRELATION FROM CIF DATA

names = ['fcc', ]  # 1al1 qmax 0.36992983463258367
nq = 100
npsi = 180
# qmax = 1.4


for name in names:
    print(f'Correlating: {name}')
    cif = scorpy.CifData(f'{__DATADIR}/xtal/{name}-sf.cif')
    print(cif.scat_sph.shape)
    corr = scorpy.CorrelationVol(nq, npsi, cif.qmax)
    corr.fill_from_cif(cif)
    corr.save(f'{__DATADIR}/dbins/{name}_qcor')
