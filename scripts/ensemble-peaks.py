import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')

corr1 = scorpy.CorrelationVol(path='../data/dbins/ensemble_peaks/ensemble_n16_0.dbin')
corr2 = scorpy.CorrelationVol(path='../data/dbins/ensemble_peaks/ensemble_n16_1.dbin')
corr3 = scorpy.CorrelationVol(path='../data/dbins/ensemble_peaks/ensemble_n16_2.dbin')



corr1.plot_sumax()
corr2.plot_sumax()
corr3.plot_sumax()



plt.show()








