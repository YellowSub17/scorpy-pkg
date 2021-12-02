

import scorpy
import matplotlib.pyplot as plt




logpath = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/mofs/hkust/x.log'




group = 'hkustcont'
tag = '500frames_a'
v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/{group}/{group}_{tag}/{group}_{tag}_padf2_padf.dbin', logpath=logpath)
v.plot_xy(title='a')

group = 'hkustcont'
tag = '500frames_b'
v = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/{group}/{group}_{tag}/{group}_{tag}_padf2_padf.dbin', logpath=logpath)
v.plot_xy(title='b')




plt.show()

