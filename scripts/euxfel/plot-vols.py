
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




# for run in runs:

    # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt')

    # frames = pk.split_frames()


    # npeaks = []

    # for frame in frames:
        # npeaks.append(frame.scat_rect.shape[0])


    # plt.figure()
    # plt.hist(npeaks, bins=100)
    # plt.title(f'{run}')



# sims = [4**i for i in range(2,6)]

sims = [16, 64, 256, 512, 1024, 2048]

print(sims)



fig, axes= plt.subplots(2,3)

for i, sim in enumerate(sims):
    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim}/sim{sim}-qcor.dbin')
    corr.vol[:,:,0] = 0
    corr.vol[:,:,-1] = 0

    corr.plot_q1q2(title=f'{sim}', log=True, fig=fig, axes=axes.flatten()[i])
plt.suptitle('Log total correlation')



fig, axes= plt.subplots(2,3)

for i, sim in enumerate(sims):
    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim}/sim{sim}-seed0a-qcor.dbin')
    # corr.vol[:,:,0] = 0
    # corr.vol[:,:,-1] = 0

    corr.plot_q1q2(title=f'{sim}', log=True, fig=fig, axes=axes.flatten()[i])
plt.suptitle('Log seed0a correlation')

fig, axes= plt.subplots(2,3)

for i, sim in enumerate(sims):
    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/qcors/sim/{sim}/sim{sim}-seed0b-qcor.dbin')
    # corr.vol[:,:,0] = 0
    # corr.vol[:,:,-1] = 0

    corr.plot_q1q2(title=f'{sim}', log=True, fig=fig, axes=axes.flatten()[i])
plt.suptitle('Log seed0b correlation')



geom = scorpy.ExpGeom(f'{scorpy.DATADIR}/geoms/agipd_2304_vj_opt_v4.geom')

plt.figure()
geom.plot_panels()

q = scorpy.utils.convert_q2r(corr.qmax, geom.clen, geom.wavelength)

geom.plot_qring(corr.qmax)




plt.show()





















plt.show()

