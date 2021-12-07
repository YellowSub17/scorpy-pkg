

import scorpy
import matplotlib.pyplot as plt




logpath = '/home/pat/Documents/cloudstor/phd/python_projects/scorpy-pkg/data/mofs/hkust/x.log'




group = 'hkustsoak'

tag = '500frames_a'
va = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/{group}/{group}_{tag}/{group}_{tag}_padf2_padf.dbin', logpath=logpath)
va.normalize()

tag = '500frames_b'
vb = scorpy.Vol(path=f'{scorpy.DATADIR}/mofs/hkust/{group}/{group}_{tag}/{group}_{tag}_padf2_padf.dbin', logpath=logpath)
vb.normalize()


vd = vb.copy()
vd.vol -=va.vol



fig, axes = plt.subplots(1,3)
va.plot_xy(title='a', fig=fig, axes=axes[0])
vb.plot_xy(title='b', fig=fig, axes=axes[1])
vd.plot_xy(title='d', fig=fig, axes=axes[2])


fig, axes = plt.subplots(1,3)
va.plot_slice(0, 100, title='a', fig=fig, axes=axes[0])
vb.plot_slice(0, 100, title='b', fig=fig, axes=axes[1])
vd.plot_slice(0, 100, title='d', fig=fig, axes=axes[2])




plt.show()

