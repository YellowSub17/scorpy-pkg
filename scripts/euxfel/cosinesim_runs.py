
import scorpy
import numpy as np
import matplotlib.pyplot as plt





qmax = 1.45
wavelength = 1.333e-10
clen = 0.1697469375
res = 5000
nq =100
npsi = 180


runs = [108, 109, 110, 113, 118, 123, 125]
# runs = [125]


for run in runs:

    # # pk = scorpy.PeakData(f'{scorpy.DATADIR}/cxi/run{run}_peaks.txt', qmax=qmax)
    # # pk.plot_peaks()

    # # plt.figure()
    # # im = pk.make_im()
    # # plt.imshow(im)
    corr = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/{run}/run{run}-qcor.dbin')
    corr.plot_q1q2(title=f'{run}', log=True)

    css_scores = []
    for seed in range(20):
        corra = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/{run}/run{run}-seed{seed}a-qcor.dbin')
        corrb = scorpy.CorrelationVol(path=f'{scorpy.DATADIR}/dbins/cxi/{run}/run{run}-seed{seed}b-qcor.dbin')


        css_scores.append(scorpy.utils.cosinesim(corra.vol, corrb.vol))

    print(f'Run: {run}')
    print(f'CSS ave: {np.average(css_scores)}')
    print(f'CSS std: {np.std(css_scores)}')

plt.show()

