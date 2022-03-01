
import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')









######3D CORR

cif = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/inten1-qmax1-sf.cif', qmax=0.264)
# geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/batch.geom')
# cif.make_saldin(k=geo.k)

corr = scorpy.CorrelationVol(qmax=0.264, nq=100, npsi=180, cos_sample=False, inc_self_corr=False)
corr.fill_from_cif(cif, verbose=2, method='scat_sph')


corr.save(f'{scorpy.DATADIR}/dbins/inten1-qmax0264-3d-sph-noselfcorr-qcor.dbin')

corr.plot_q1q2()
corr.plot_q1q2(log=True)








plt.show()
