
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys









sim_n = 128
wavelength = 6.7018e-11*1e10
npsi= 90
part = 'p0'




corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-{part}-qcor.dbin'
padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-{part}-padf.dbin'


padf = scorpy.PadfVol(path=padf_path)



fig, axes = plt.subplots(1,1)





padf.plot_xy(vminmax=(-2.5e64, 6.0e64), fig=fig, axes=axes )


# cs = [15]
# for c in cs:
    # r = c/(2*np.sin(padf.zpts/2))
    # axes.plot(padf.zpts, r, 'r')

# axes.set_ylim([0, padf.xmax])




plt.show()















