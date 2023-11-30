import scorpy
import numpy as np
import matplotlib.pyplot as plt





data_dir = '/home/ec2-user/corr/data'



xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'
super_chunk = 'x1'
chunk = 100
frame = 200



path=f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}/{chunk}'
filename = f'{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}-qcor'
corr = scorpy.CorrelationVol(path=f'{path}/{filename}')
corr.plot_q1q2()

xtal_size= '100nm'
geom_code = '19MPz040'
pdb_code = '193l'
super_chunk = 'x1'
chunk = 200
frame = 300



path=f'{data_dir}/qcor/{xtal_size}-{geom_code}-{super_chunk}/{chunk}'
filename = f'{pdb_code}-{xtal_size}-{geom_code}-{super_chunk}-{chunk}-{frame}-qcor'
corr = scorpy.CorrelationVol(path=f'{path}/{filename}')
corr.plot_q1q2()

plt.show()
