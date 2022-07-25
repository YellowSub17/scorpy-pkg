
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

import sys
import os



wavelength = 6.7018e-11*1e10
npsi= 90

nr = 500
npsi = 90
rmax = 20
nl = 64



sim_n = 2048
p = 0

corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-alpha-p{p}-qcor.dbin'
padf_path = f'{scorpy.DATADIR}/dbins/x.dbin'

print(f'!!!!#######{p=}, {sim_n=}')
print(f'!!!!#######')
print(f'!!!!#######')
corr = scorpy.CorrelationVol(path=corr_path)
padf = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)
padf.fill_from_corr(corr, theta0=False, verbose=99, tag=f'x')
# padf.save(padf_path)
print(f'!!!!#######')
print(f'!!!!#######')





