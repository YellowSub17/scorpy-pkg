
import scorpy
import numpy as np

import matplotlib.pyplot as plt




run = 118
qmax = 1.44

pk = scorpy.PeakData(f'{scorpy.DATADIR}cxi/run{run}_peaks.txt', qmax=qmax)


pk.plot_peaks(scatter=True, s=200)



corr = scorpy.CorrelationVol(qmax=qmax, cos_sample=False)

corr.fill_from_peakdata(pk, npeakmax=100)



plt.show()



