

import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np




logpath = f'{scorpy.DATADIR}/mofs/nu_n128.log'


group = 'hkustcont_4kframes'
padf_tag = 'padfcorr_correlation_sum'


vminmax = -1e-5, 1e-5

fpath = f'{scorpy.DATADIR}/mofs/hkust/{group}_a/{group}_a_{padf_tag}.dbin'
corr1 = scorpy.Vol(path=fpath, logpath=logpath)
# corr1 = corr1.crop(0, 0, 0, int(corr1.nx/2), int(corr1.ny/2), int(corr1.nz/2))
corr1.normalize()
corr1.plot_xy(vminmax = vminmax, subtmean=True)



fpath = f'{scorpy.DATADIR}/mofs/hkust/{group}_b/{group}_b_{padf_tag}.dbin'
corr1 = scorpy.Vol(path=fpath, logpath=logpath)
# corr1 = corr1.crop(0, 0, 0, int(corr1.nx/2), int(corr1.ny/2), int(corr1.nz/2))
corr1.normalize()
corr1.plot_xy(vminmax = vminmax, subtmean=True)







plt.show()

