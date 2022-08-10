
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




# nqs = list(range(25, 251, 25))
nqs = [25,50, 75, 100, 150, 200, 250]




cmap_rf = cm.winter( np.linspace(0, 1, len(nqs)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nqs)))



fig, axes = plt.subplots(2,1, figsize=(5, 5), sharex=True)
fig.tight_layout()
fig.subplots_adjust(
    top=0.951,
    bottom=0.091,
    left=0.116,
    right=0.993,
    hspace=0.04,
    wspace=0.0
)

for i, nq in enumerate(nqs):
    print(nq)
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'rfs', marker='',linestyle='-', fig=fig, axes=axes[0], color = cmap_rf[i], label=f'{nq}', ylabel='$R_f$')

    a.plot_vs_count('a', 'mean_dxyzs', marker='',linestyle='-',fig=fig, axes=axes[1], color = cmap_atomic[i], label=f'{nq}', ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration')

axes[0].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1)
axes[1].legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1)
axes[0].set_title('Algorithm Accuracy as a Function of nq Sampling')





plt.show()



fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nq-test.png', dpi=300)

