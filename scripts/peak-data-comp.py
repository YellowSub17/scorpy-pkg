import scorpy
import numpy as np
import matplotlib.pyplot as plt





cor1 = scorpy.CorrelationVol(path="../data/dbins/cosine_sim/102/run102_qcor")
cor2 = scorpy.CorrelationVol(path="../data/dbins/cosine_sim/120/run120_qcor")



cor1.plot_sumax()
cor2.plot_sumax()
plt.show()

