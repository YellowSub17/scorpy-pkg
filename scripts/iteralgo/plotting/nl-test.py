
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




nls = list(range(60, 181, 15))

cmap = cm.jet( np.linspace(0, 1, len(nls)))





fig1, axes1 = plt.subplots(1,1)

for i, nl in enumerate(nls):
    print(nl)
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    a.plot_vs_count('a', 'rfs', marker='.', fig=fig1, axes=axes1, color = cmap[i], label=f'{nl}', ylabel='$R_f$', xlabel='Iteration')

fig2, axes2 = plt.subplots(1,2)

for i, nl in enumerate(nls):
    print(nl)
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    a.plot_vs_count('a', 'mean_dxyzs', marker='.',fig=fig2, axes=axes2[0], color = cmap[i], label=f'{nl}', ylabel='Mean Atomic Displacement', xlabel='Iteration')
    a.plot_vs_count('a', 'mean_ddistances', marker='.',fig=fig2, axes=axes2[1], color = cmap[i], label=f'{nl}', ylabel='Mean $\\Delta$ Bond Length', xlabel='Iteration')



plt.legend()
plt.show()

