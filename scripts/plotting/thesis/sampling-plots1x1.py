
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np

plt.rc('font', size=8)



# nqs = list(range(25, 251, 25))
# nqs = [25,50, 75, 100, 150, 200, 250]
nqs = [ 50, 75,  100, 125, 150, 200]
# nls = list(range(60, 181, 15))

nls = [60, 90, 120, 135, 150, 180]


cmap_rf = cm.winter( np.linspace(0, 1, len(nqs)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nqs)))


#### nq
# fig, axes = plt.subplots(2,1, figsize=(7.87, 2*3.93), dpi=150, sharex=True)




plt.rc('font', size=8)
fignqrf, axesnqrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )
fignqd, axesnqd = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )


for i, nq in enumerate(nqs):
    print(f'{nq=}')
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'rfs', marker=',',linestyle='-',
                    fig=fignqrf, axes=axesnqrf,  ylabel='$R_f$',color=cmap_rf[i],
                    xerr=None, yerr=None, label=f'{nq}', xlabel='Algorithm Iteration')


    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker=',', linestyle='-',
                    fig=fignqd, axes=axesnqd, color = cmap_atomic[i], ylabel='Mean Atomic Displacement [\u212B]',
                    xerr=None, yerr=None, label=f'{nq}', xlabel='Algorithm Iteration')


axesnqrf.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              )
axesnqd.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              )

axesnqrf.set_xlim(0.5, 110.5)
axesnqd.set_xlim(0.5, 110.5)
axesnqrf.set_ylim(0.145, 0.5)
axesnqd.set_ylim(0, 1.16)


fignqrf.tight_layout()
fignqd.tight_layout()
fignqrf.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_samp_nqrf.png')
fignqd.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_samp_nqd.png')







cmap_rf = cm.winter( np.linspace(0, 1, len(nls)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nls)))



# #### nl
# fig, axes = plt.subplots(2,1,figsize=(16/2.54, 8/2.54), dpi=300, sharex=True)

fignlrf, axesnlrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )
fignld, axesnld = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )





for i, nl in enumerate(nls):
    print(f'{nl=}')
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')

    a.plot_vs_count('a', 'rfs', marker='',linestyle='-',
                    fig=fignlrf, axes=axesnlrf, color = cmap_rf[i], ylabel='$R_f$',
                   xerr=None, yerr=None, xlabel='Algorithm Iteration', label=f'{nl}')

    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker='',linestyle='-', label=f'{nl}',
                    fig=fignld, axes=axesnld, color = cmap_atomic[i], xerr=None, yerr=None,
                    ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration')

axesnlrf.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              )

axesnld.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              )

axesnlrf.set_xlim(0.5, 110)
axesnld.set_xlim(0.5, 110)
axesnlrf.set_ylim(0.145, 0.5)
axesnld.set_ylim(0, 1.16)


fignlrf.tight_layout()
fignld.tight_layout()

fignlrf.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_samp_nlrf.png')
fignld.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_samp_nld.png')
plt.show()


