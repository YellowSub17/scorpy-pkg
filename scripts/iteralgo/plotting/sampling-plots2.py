
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




# nqs = list(range(25, 251, 25))
# nqs = [25,50, 75, 100, 150, 200, 250]
nqs = [50, 75,  100, 150, 200]
# nls = list(range(60, 181, 15))

nls = [60, 90, 120, 150, 180]


cmap_rf = cm.winter( np.linspace(0, 1, len(nqs)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nqs)))




#### nq
fig, axes = plt.subplots(2,2, figsize=(7.87, 4*3.93), dpi=150, sharex=True,)


for i, nq in enumerate(nqs):
    print(f'{nq=}')
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'rfs', marker='',linestyle='-', fig=fig, axes=axes[0,0], color = cmap_rf[i], label=f'{nq}', ylabel='$R_f$')
    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker='',linestyle='-',fig=fig, axes=axes[0, 1], color = cmap_atomic[i], label=f'{nq}', ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration')

axes[0,0].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$')
axes[0,1].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nq$')
axes[0,0].set_title('Radial Sampling')

fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nq-test.png')
fig.tight_layout()







cmap_rf = cm.winter( np.linspace(0, 1, len(nls)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nls)))



# #### nl
# fig, axes = plt.subplots(2,1, figsize=(7.87, 2*3.93),dpi=150, sharex=True)




for i, nl in enumerate(nls):
    print(f'{nl=}')
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')

    a.plot_vs_count('a', 'rfs', marker='',linestyle='-', fig=fig, axes=axes[1,0], color = cmap_rf[i], label=f'{nl}', ylabel='$R_f$')

    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker='',linestyle='-',fig=fig, axes=axes[1,1], color = cmap_atomic[i], label=f'{nl}', ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration')



axes[1,0].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$')
axes[1,1].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$nL$')
axes[1,0].set_title('Angluar Sampling')
fig.tight_layout()



fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nl-test.png')



plt.show()




