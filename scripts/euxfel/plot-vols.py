
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys









sim_n = sys.argv[1]


for part in sys.argv[2:]:
    corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p{part}-qcor.dbin'
    padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p{part}-padf.dbin'


    padf = scorpy.PadfVol(path=padf_path)
    padf = padf.crop(0, 0, 0, 150,150, padf.nz-1)


    fig, axes = plt.subplots(1,1)
    padf.plot_xy(vminmax=(-2.5e64, 12.0e64), fig=fig, axes=axes )
    rc = 6.5/(2*np.sin(padf.zpts[5:]/2))
    axes.plot(padf.zpts[5:], rc)
    axes.set_ylim(0, padf.ymax)




# for run in sys.argv[1:]:
    # # corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p{part}-qcor.dbin'
    # corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin'
    # padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin'


    # padf = scorpy.PadfVol(path=padf_path)
    # padf = padf.crop(0, 0, 0, 150,150, padf.nz-1)

    # fig, axes = plt.subplots(1,1)
    # padf.plot_xy(vminmax=(-2.5e64, 12.0e64), fig=fig, axes=axes )
    # rc = 6.5/(2*np.sin(padf.zpts[5:]/2))
    # axes.plot(padf.zpts[5:], rc)
    # axes.set_ylim(0, padf.ymax)


plt.show()















