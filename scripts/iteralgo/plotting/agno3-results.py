
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np






subtags = 'abcdefgh'

subtags=['aER', 'bER', 'cER', 'dER', 'eER', 'fER', 'gER', 'hER',
         'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']


cmap = cm.jet( np.linspace(0, 1, len(subtags)))




fig1, axes1 = plt.subplots(1,1)
for i, subtag in enumerate(subtags):

    a = scorpy.AlgoHandler(f'agno3-d03')
    a.plot_vs_count(subtag, 'rfs', marker='.', fig=fig1, axes=axes1, color = cmap[i], label=f'{subtag}', ylabel='$R_f$', xlabel='Iteration')
plt.legend()

fig2, axes2 = plt.subplots(1,2)
for i, subtag in enumerate(subtags):
    a = scorpy.AlgoHandler(f'agno3-d03')
    a.plot_vs_count(subtag, 'mean_dxyzs', marker='.',fig=fig2, axes=axes2[0], color = cmap[i], label=f'{subtag}', ylabel='Mean Atomic Displacement', xlabel='Iteration')
    a.plot_vs_count(subtag, 'mean_ddistances', marker='.',fig=fig2, axes=axes2[1], color = cmap[i], label=f'{subtag}', ylabel='Mean $\\Delta$ Bond Length', xlabel='Iteration')
plt.legend()







# fig1, axes1 = plt.subplots(1,1)
# for i, subtag in enumerate(subtags):

    # a = scorpy.AlgoHandler(f'agno3-d03')
    # a.plot_vs_count(subtag+'ER', 'rfs', marker='.', fig=fig1, axes=axes1, color = cmap[i], label=f'{subtag}ER', ylabel='$R_f$', xlabel='Iteration')
# plt.legend()

# fig2, axes2 = plt.subplots(1,2)
# for i, subtag in enumerate(subtags):
    # a = scorpy.AlgoHandler(f'agno3-d03')
    # a.plot_vs_count(subtag+'ER', 'mean_dxyzs', marker='.',fig=fig2, axes=axes2[0], color = cmap[i], label=f'{subtag}ER', ylabel='Mean Atomic Displacement', xlabel='Iteration')
    # a.plot_vs_count(subtag+'ER', 'mean_ddistances', marker='.',fig=fig2, axes=axes2[1], color = cmap[i], label=f'{subtag}ER', ylabel='Mean $\\Delta$ Bond Length', xlabel='Iteration')
# plt.legend()










plt.show()

