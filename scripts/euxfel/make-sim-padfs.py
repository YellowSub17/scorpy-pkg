
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

import sys
import os



sim_n = 2048
wavelength = 6.7018e-11*1e10
npsi= 90
part = 'p1'



rmaxs = [86/2, 86/3, 86/4, 86/5, 86/6, 86/7, 86/8]
nrs = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
nls = [12, 16, 20, 24, 28, 32, 36, 40, 44, 48]


rmax_i = sys.argv[1]
nr_i = sys.argv[2]
nl_i = sys.argv[3]



code = f'code_{rmax_i}{nr_i}{nl_i}'
print(f'##################{code}')
nr = nrs[int(nr_i)]
nl = nls[int(nl_i)]
rmax = rmaxs[int(rmax_i)]



# rmax = 86/2
# npsi_r = 90
# nr = 200
# nl = 32


corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-{part}-qcor.dbin'
padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-{part}-{code}-padf.dbin'




corr = scorpy.CorrelationVol(path=corr_path)

padf = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)
padf.fill_from_corr(corr, theta0=False, verbose=99, tag=part)
padf.save(padf_path)






