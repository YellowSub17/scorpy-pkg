
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')



nr =250
npsi = 180

nl = 36
rmax = 6 #A
wavelength = 1.33


sim_n = 2048

corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p0-qcor.dbin'
padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p0-padf.dbin'

corr = scorpy.CorrelationVol(path=corr_path)
padf = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)

padf.fill_from_corr(corr, log=None, theta0=False)
padf.save(padf_path)

padf.plot_r1r2( vminmax=(0,7e69))




corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p1-qcor.dbin'
padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p1-padf.dbin'

corr = scorpy.CorrelationVol(path=corr_path)
padf = scorpy.PadfVol(nr=nr, npsi=npsi, rmax=rmax, nl=nl, wavelength=wavelength)

padf.fill_from_corr(corr, log=None, theta0=False)
padf.save(padf_path)

padf.plot_r1r2( vminmax=(0,7e69))
plt.show()





