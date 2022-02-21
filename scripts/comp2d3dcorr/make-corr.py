
import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')









######3D CORR

geo = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/single_square.geom')
cif = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/1vds-qmax1-sf.cif', qmax=1)
cif.make_saldin(k=geo.k)

corr = scorpy.CorrelationVol(qmax=cif.qmax, nq=100, npsi=180, cos_sample=False, inc_self_corr=False)
corr.fill_from_cif(cif, verbose=2, method='scat_sph')


corr.save(f'{scorpy.DATADIR}/dbins/1vds-3d-ssph-qcor.dbin')

corr.plot_q1q2()
corr.plot_q1q2(log=True)








plt.show()
