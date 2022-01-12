

import scorpy
import matplotlib.pyplot as plt
plt.close('all')
import numpy as np




logpath = f'{scorpy.DATADIR}/mofs/nu_n512.log'

group = 'hkustcont_4kframes'
padf_tag = 'padf2_padf'



vminmax = 0.1, 0.3

fpath = f'{scorpy.DATADIR}/mofs/hkust/{group}_a/{group}_a_{padf_tag}.dbin'
padf1 = scorpy.Vol(path=fpath, logpath=logpath)
padf1 = padf1.crop(0, 0, 0, int(padf1.nx/4), int(padf1.ny/4), int(padf1.nz/2))
padf1.normalize()
padf1.plot_xy(vminmax = vminmax)


# fpath = f'{scorpy.DATADIR}/mofs/hkust/{group}_b/{group}_b_{padf_tag}.dbin'
# padf1 = scorpy.Vol(path=fpath, logpath=logpath)
# padf1 = padf1.crop(0, 0, 0, int(padf1.nx/4), int(padf1.ny/4), int(padf1.nz/2))
# padf1.normalize()
# padf1.plot_xy(vminmax = vminmax)




plt.show()

