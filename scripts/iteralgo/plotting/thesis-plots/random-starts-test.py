
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




# nqs = list(range(25, 251, 25))











subtags = 'abcdefgh'
# cmap = cm.Set1( np.linspace(0, 1, len(subtags)))
# cmap = cm.tab10( np.linspace(0, 1, len(subtags)))
cmap1 = cm.afmhot( np.linspace(0.2, 0.7, len(subtags)))
cmap2 = cm.cool( np.linspace(0.2, 0.7, len(subtags)))

plt.rc('font', size=8)
fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300)

for i, subtag in enumerate(subtags):
    print(subtag)
    a = scorpy.AlgoHandler(f'agno3-d03')
    a.plot_vs_count(f'{subtag}', 'rfs',marker='.', linestyle='', markersize=1, color = cmap1[i],
                    fig=fig, axes=axes,
                    label=f'{subtag}', ylabel='$R_f$', xlabel='Algorithm Iteration', xerr=None, yerr=None)

    a.plot_vs_count(f'{subtag}ER', 'rfs',marker='.', linestyle='', markersize=1, color = cmap2[i],
                    fig=fig, axes=axes,
                    label=f'{subtag}ER', ylabel='$R_f$', xlabel='Algorithm Iteration', xerr=None, yerr=None)


axes.set_xlim(0.5, 240)
axes.set_ylim(0.19, 0.45)

plt.tight_layout()


fig.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/algo_random_rfs.png')

fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300)

for i, subtag in enumerate(subtags):
    print(subtag)
    a = scorpy.AlgoHandler(f'agno3-d03')
    a.plot_vs_count(f'{subtag}', 'mean_dxyzs',marker='.', linestyle='', markersize=1, color = cmap1[i],
                    fig=fig, axes=axes,
                    label=f'{subtag}', ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration', xerr=None, yerr=None)

    a.plot_vs_count(f'{subtag}ER', 'mean_dxyzs',marker='.', linestyle='', markersize=1, color = cmap2[i],
                    fig=fig, axes=axes,
                    label=f'{subtag}ER', ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration', xerr=None, yerr=None)



axes.set_xlim(0.5, 240)
axes.set_ylim(0, .5)

plt.tight_layout()
fig.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/algo_random_d.png')

plt.show()

