
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np




nls = list(range(60, 181, 15))

cmap = cm.jet( np.linspace(0, 1, len(nls)))





fig, axes = plt.subplots(1,1)

for i, nl in enumerate(nls):
    print(nl)

    a = scorpy.AlgoHandler(f'agno3-nl{nl}')
    # a.plot_mean_dxyzs('a',fig=fig, axes=axes, color = cmap[i], label=f'{nl}',dx=0.1*i, title='mean atomic displacement')
    a.plot_vs_count('b', 'std_ddistances',marker='.',fig=fig, axes=axes, color = cmap[i], label=f'{nl}')
    a.plot_vs_count('b', 'max_ddistances',marker='x',fig=fig, axes=axes, color = cmap[i], label=f'{nl}')



plt.legend()
plt.show()

