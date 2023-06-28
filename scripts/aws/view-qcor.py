import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'
xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'

chunk = 0
frame = 100







corr_dir =  f'{data_dir}/qcor/{xtal_size}-{geom_code}'
corr = scorpy.CorrelationVol(path=f'{corr_dir}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{chunk}-{frame}-qcor.npy')

corr._plot_2D(corr.get_xy(), vminmax=(10,100))


npz_fname =  f'{data_dir}/frames/{xtal_size}-{geom_code}/{chunk}/{pdb_code}-{xtal_size}-{geom_code}-{chunk}-{frame}.npz'
pk = scorpy.PeakData(npz_fname, f'/home/ec2-user/corr/data/geom/19MPz040.geom')
pk.plot_peaks()


pk.plot_qring(q=corr.qpts[40])
pk.plot_qring(q=corr.qpts[106])
pk.plot_qring(q=corr.qpts[112])

plt.show()



