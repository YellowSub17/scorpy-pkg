
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches





qmax = 1.45
wavelength = 1.333e-10




runs = [108,113,109,125,110,123,118,112,119,120,102,104,105,103,121,126]




# runs = runs[:4]

# ### plot corrs
# for run in runs:

    # corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/{run}/run{run}-qcor.dbin')
    # corr.plot_q1q2(title=f'{run}', log=True)


# for run in runs:
    # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)
    # print(pk.scat_rect.shape)


#### plot padf
# fig, axes = plt.subplots(2,2)
# for i, run in enumerate(runs):
    # padf = scorpy.PadfVol(path=f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin')
    # padf._zmax=180

    # padf.plot_xy(vminmax=(-1e70, 2.5e71), title=f'{run}', fig=fig, axes=axes.flatten()[i])


fig, axes = plt.subplots(4,4)
for i, run in enumerate(runs):
    padf = scorpy.PadfVol(path=f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin')
    padf._zmax=180

    padf = padf.crop(40,40,0,149,149,89)
    padf.plot_xy(vminmax=(-1e70, 2.5e70), title=f'{run}', fig=fig, axes=axes.flatten()[i])
    # padf.plot_xy(title=f'{run}', fig=fig, axes=axes.flatten()[i])

    # axes.flatten()[i].plot(47.9, 1.835, 'r.')
    # axes.flatten()[i].plot(46.8, 1.384, 'r.')





fig, axes = plt.subplots(2,2)
for i, run in enumerate(runs):
    padf = scorpy.PadfVol(path=f'{scorpy.DATADIR}/dbins/cxi/padfs/{run}/run{run}-padf.dbin')
    padf.plot_r1r2( title=f'{run}', fig=fig, axes=axes.flatten()[i])





plt.show()

