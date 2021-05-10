

import numpy as np

import scorpy
import matplotlib.pyplot as plt


corr1 = scorpy.CorrelationVol(path='../data/dbins/1vds_qcor.dbin')
corr2 = scorpy.CorrelationVol(path='../data/dbins/1vds_fj_qcor.dbin')

corr1.plot_q1q2()
corr2.plot_q1q2()
plt.show()
