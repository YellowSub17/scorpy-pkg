
import scorpy
import numpy as np

import matplotlib.pyplot as plt




qmax = 1.44



# runs = [108, 109, 110, 113, 118, 123, 125]

runs = [118]

for run in runs:

    print(f'####### Run {run}')
    pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)

    corr = scorpy.CorrelationVol(qmax=qmax, cos_sample=False, inc_self_corr=True)
    corr.fill_from_peakdata(pk, npeakmax=150, method='scat_pol')
    # corr.save(f'../../data/dbins/cxi/run{run}_qcor.dbin')

corr.plot_q1q2()





plt.show()



