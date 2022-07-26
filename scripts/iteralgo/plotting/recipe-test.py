
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np





subtags = ['ER120',
            'HIO10ER10',
            'HIO20ER20',
            'HIO30ER30',
            'HIO60ER60',
            'HIO120',
           ]






cmap = cm.jet( np.linspace(0, 1, len(subtags)))





fig1, axes1 = plt.subplots(1,1)

for i, subtag in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    a.plot_vs_count(f'{subtag}', 'rfs', marker='.', fig=fig1, axes=axes1, color = cmap[i], label=f'{subtag}', ylabel='$R_f$', xlabel='Iteration')
plt.legend()

fig2, axes2 = plt.subplots(1,2)

for i, subtag in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    a.plot_vs_count(f'{subtag}', 'mean_dxyzs', marker='.',fig=fig2, axes=axes2[0], color = cmap[i], label=f'{subtag}', ylabel='Mean Atomic Displacement', xlabel='Iteration')
    a.plot_vs_count(f'{subtag}', 'mean_ddistances', marker='.',fig=fig2, axes=axes2[1], color = cmap[i], label=f'{subtag}', ylabel='Mean $\\Delta$ Bond Length', xlabel='Iteration')



plt.legend()
plt.show()

