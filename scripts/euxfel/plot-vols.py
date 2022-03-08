
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches





qmax = 1.45
wavelength = 1.333e-10




runs = [108,113,109,125,110,123,118,112,119,120,102,104,105,103,121,126]




# n = 4

# seed = 5

# corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-qcor.dbin')


# corr.plot_sumax(0,log=True)


# corra = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}a-qcor.dbin')
# corra.plot_sumax(0,log=True)
# corrb = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{n}/sim{n}-seed{seed}b-qcor.dbin')
# corrb.plot_sumax(0,log=True)




for run in runs:

    pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt')

    frames = pk.split_frames()


    npeaks = []

    for frame in frames:
        npeaks.append(frame.scat_rect.shape[0])


    plt.figure()
    plt.hist(npeaks, bins=100)
    plt.title(f'{run}')

















plt.show()

