
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np

plt.rc('font', size=8)



nqs = list(range(25, 251, 25))
nls = list(range(60, 181, 15))

# nqs = [ 50, 75,  100, 125, 150, 200]
# nls = [60, 90, 120, 135, 150, 180]


cmap_nq = cm.winter( np.linspace(0, 1, len(nqs)))
cmap_nl = cm.gist_heat( np.linspace(0, 0.75, len(nls)))


#### nq
# fig, axes = plt.subplots(2,1, figsize=(7.87, 2*3.93), dpi=150, sharex=True)



fig, axes = plt.subplots(2,2,figsize=(16/2.54, 14/2.54), dpi=300, sharex='col', sharey='row')


for i, nq in enumerate(nqs):
    print(f'{nq=}')
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'rfs', marker=',',linestyle='-',
                    fig=fig, axes=axes[1,0],  ylabel='$R_f$',color=cmap_nq[i],
                    xerr=None, yerr=None,xlabel='Algorithm Iteration')
    # axes[1,0].plot(105, 0.45, color=cmap_nq[i], label=f'{nq}', marker='.',)


    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker=',', linestyle='-',
                    fig=fig, axes=axes[0,0], color = cmap_nq[i], ylabel='Mean Atomic Displacement [\u212B]',
                     xerr=None, yerr=None)
    axes[0,0].plot(105, 1, color=cmap_nq[i], label=f'{nq}', marker='.',linestyle='')

axes[0,0].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$', ncol=2,
    borderpad=0.5,
    labelspacing=0,
    handlelength=0,
    handletextpad=0.5,
    columnspacing=1.5
              )
# axes[1,0].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              # )




# fig.tight_layout()
# fig.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/algo_samp_nq.png')










# #### nl
# fig, axes = plt.subplots(2,1,figsize=(16/2.54, 8/2.54), dpi=300, sharex=True)




for i, nl in enumerate(nls):
    print(f'{nl=}')
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')

    a.plot_vs_count('a', 'rfs', marker='',linestyle='-',
                    fig=fig, axes=axes[1,1], color = cmap_nl[i], ylabel='',
                   xerr=None, yerr=None, xlabel='Algorithm Iteration')

    # axes[1,1].plot(105, 0.45, color=cmap_nl[i], label=f'{nl}', marker='.',)
    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker='',linestyle='-',
                    fig=fig, axes=axes[0,1], color = cmap_nl[i], xerr=None, yerr=None,
                    ylabel='')

    axes[0,1].plot(105, 1, color=cmap_nl[i], label=f'{nl}', marker='.',linestyle='')



axes[0,1].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$', ncol=1,
    borderpad=0.5,
    labelspacing=0,
    handlelength=0,
    handletextpad=0.5,
    columnspacing=1.5
              )

# axes[1,1].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$', ncol=2,
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              # )
axes[0,0].set_xlim(0.5, 110.5)
axes[0,1].set_xlim(0.5, 80)
axes[1,1].set_ylim(0.145, 0.55)
axes[0,1].set_ylim(0, 1.16)



fig.tight_layout()


fig.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/algo_samp.png')


import os
os.system('xdg-open /home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/algo_samp.png')



plt.show()




