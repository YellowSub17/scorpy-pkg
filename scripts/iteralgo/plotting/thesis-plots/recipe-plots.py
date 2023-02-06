
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np





subtags = [('ER120','P'),
           ('HIO10ER10','X'),
           ('HIO20ER20','*'),
           ('HIO30ER30','h'),
           ('HIO120','o'),
           ]




cmap_rf = cm.winter( np.linspace(0, 1, len(subtags)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(subtags)))



fig, axes = plt.subplots(2,1, figsize=(7.87, 2*3.93),dpi=150, sharex=True)


for i, (subtag, marker) in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    a.plot_vs_count(f'{subtag}', 'rfs', marker='', linestyle='-',  fig=fig, axes=axes[0], color = cmap_rf[i], label=f'{subtag}', ylabel='$R_f$')


    a.plot_vs_count(f'{subtag}', 'mean_dxyzs', marker='', linestyle='-', fig=fig, axes=axes[1], color =cmap_atomic[i], label=f'{subtag}', ylabel='Mean Atomic Displacement', xlabel='Iteration', logy=False)

# axes[0].legend(bbox_to_anchor=(1,1), loc="upper left")
# axes[1].legend(bbox_to_anchor=(1,1), loc="upper left")

axes[0].legend(loc="upper right", title='Iterative Scheme')
axes[1].legend(loc="upper right", title='Iterative Scheme')
axes[0].set_title('Iterative Algorithm Recipes')

plt.tight_layout()


fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/recipes.png')



plt.show()

