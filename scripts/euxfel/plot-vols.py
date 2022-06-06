
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import sys









# sim_n = sys.argv[1]


# for part in sys.argv[2:]:
    # corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p{part}-qcor.dbin'
    # padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/sim/{sim_n}/sim{sim_n}-p{part}-padf.dbin'


    # padf = scorpy.PadfVol(path=padf_path)

    # fig, axes = plt.subplots(1,1)


    # padf.plot_xy(vminmax=(-2.5e64, 12.0e63), fig=fig, axes=axes )




for run in sys.argv[1:]:
    # corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim_n}/sim{sim_n}-p{part}-qcor.dbin'
    corr_path = f'{scorpy.DATADIR}/dbins/cxi/qcors/{run}/run{run}-qcor.dbin'
    padf_path = f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin'


    padf = scorpy.PadfVol(path=padf_path)

    fig, axes = plt.subplots(1,1)


    padf.plot_xy(vminmax=(-2.5e64, 12.0e63), fig=fig, axes=axes )


plt.show()















