
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np





subtags = [('ER120','P'), 
           ('HIO10ER10','X'), 
           ('HIO20ER20','*'), 
           ('HIO30ER30','h'), 
           ('HIO60ER60','^'), 
           ('HIO120','o'), 
           ]




cmap_rf = cm.winter( np.linspace(0, 1, len(subtags)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(subtags)))



fig, axes = plt.subplots(2,1, figsize=(9, 6), sharex=True)
plt.tight_layout()
plt.subplots_adjust(
    top=0.966,
    bottom=0.076,
    left=0.073,
    right=0.903,
    hspace=0.04,
    wspace=0.0
)



for i, (subtag, marker) in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    a.plot_vs_count(f'{subtag}', 'rfs', marker='', linestyle='-',  fig=fig, axes=axes[0], color = cmap_rf[i], label=f'{subtag}', ylabel='$R_f$')


    a.plot_vs_count(f'{subtag}', 'mean_dxyzs', marker='', linestyle='-', fig=fig, axes=axes[1], color =cmap_atomic[i], label=f'{subtag}', ylabel='Mean Atomic Displacement', xlabel='Iteration')

axes[0].legend(bbox_to_anchor=(1,1), loc="upper left")
axes[1].legend(bbox_to_anchor=(1,1), loc="upper left")
axes[0].set_title('Algorithm Accuracy as a Function of nq Sampling')





plt.show()

