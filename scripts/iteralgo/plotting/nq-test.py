
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




nqs = list(range(25, 251, 25))




cmap = cm.jet( np.linspace(0, 1, len(nqs)))





fig1, axes1 = plt.subplots(1,1)

for i, nq in enumerate(nqs):
    print(nq)
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'rfs', marker='.', fig=fig1, axes=axes1, color = cmap[i], label=f'{nq}', ylabel='$R_f$', xlabel='Iteration')
plt.legend()

fig2, axes2 = plt.subplots(1,2)

for i, nq in enumerate(nqs):
    print(nq)
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    a.plot_vs_count('a', 'mean_dxyzs', marker='.',fig=fig2, axes=axes2[0], color = cmap[i], label=f'{nq}', ylabel='Mean Atomic Displacement', xlabel='Iteration')
    a.plot_vs_count('a', 'mean_ddistances', marker='.',fig=fig2, axes=axes2[1], color = cmap[i], label=f'{nq}', ylabel='Mean $\\Delta$ Bond Length', xlabel='Iteration')



plt.legend()
plt.show()

