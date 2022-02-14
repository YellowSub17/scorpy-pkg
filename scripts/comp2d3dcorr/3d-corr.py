



import numpy as np
import scorpy
import matplotlib.pyplot as plt
plt.close('all')




cif = scorpy.CifData(path=f'{scorpy.DATADIR}/cifs/1vds-sf.cif', qmax=1)

print(cif.scat_rect.shape)


corr = scorpy.CorrelationVol(qmax=cif.qmax)
corr.fill_from_cif(cif, verbose=2)

corr.save(f'{scorpy.DATADIR}/dbins/1vds-qcor.dbin')
corr.plot_q1q2()
plt.show()


