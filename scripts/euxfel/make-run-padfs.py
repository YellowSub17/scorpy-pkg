#!/usr/bin/env python3
import scorpy
import numpy as np
import time

import os
import matplotlib.pyplot as plt
plt.close('all')



nr =250
npsi = 90
nl = 31
rmax = 6
wavelength = 1.33







runs = [108,113,109,125,110,123,118,112,119,120,102,104,105,103,121,126]


# runs = runs[:4]






for run in runs:
    print(run)
    padf = scorpy.PadfVol(nr, npsi, rmax, nl, wavelength)
    padf.fill_from_corr(f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin', log=None)
    padf.save(f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin')









