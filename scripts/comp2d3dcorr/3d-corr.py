



import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')




cif = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/1vds-sf.cif', qmax=1)
cif.make_saldin()



corr = scorpy.CorrelationVol(qmax=cif.qmax, nq=100, npsi=180, cos_sample=False, inc_self_corr=False)
corr.fill_from_cif(cif, verbose=2, method='scat_pol')

corr.save(f'{scorpy.DATADIR}/dbins/1vds-3d-qcor.dbin')
corr.plot_q1q2()
corr.plot_q1q2(log=True)
plt.show()


