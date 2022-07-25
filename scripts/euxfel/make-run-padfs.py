#!/usr/bin/env python3
import scorpy
import numpy as np
import time

import os
import matplotlib.pyplot as plt
plt.close('all')



wavelength = 6.7018e-11*1e10
npsi= 90



nr = 500
npsi = 90
rmax = 86
nl = 56






runs = [108,113,109,125,110,123,118,112,119,120,102,104,105,103,121,126]








for run in runs:
    corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin'
    padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin'

    print(f'!!!!#######{run=}')
    print(f'!!!!#######')
    print(f'!!!!#######')
    corr = scorpy.CorrelationVol(path=corr_path)
    padf = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)
    padf.fill_from_corr(corr, theta0=False, verbose=99, tag=f'run{run}')
    padf.save(padf_path)
    print(f'!!!!#######')
    print(f'!!!!#######')













