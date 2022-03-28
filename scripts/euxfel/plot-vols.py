
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches





qmax = 1.45
wavelength = 1.333e-10








run = 113


corr1 = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin')


corr1.plot_slice(2, 1, log=True)




corr2 = scorpy.CorrelationVol(path=f'/home/pat/Desktop/qcors.bkup/{run}/run{run}-qcor.dbin')
corr2.plot_slice(2,1, log=True)














plt.show()





















plt.show()

