import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'
super_chunk = 'x1'




corra = scorpy.CorrelationVol(path=f'{data_dir}/qcor/nsums/193l-80nm-19MPz040-x1-n32768-s1-qcor.dbin')

corra.qpsi_correction()
corra.plot_q1q2(vminmax=(0, 1e7))

plt.show()
