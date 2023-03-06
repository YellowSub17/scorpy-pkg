
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np





subtags = [('ER120','120 ER'),
           ('HIO10ER10','(10 HIO + 10 ER) x12'),
           ('HIO20ER20','(20 HIO + 20 ER) x6'),
           ('HIO30ER30','(30 HIO + 30 ER) x3'),
           ('HIO120','120 HIO')
           ]




cmap_rf = cm.winter( np.linspace(0, 1, len(subtags)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(subtags)))



plt.rc('font', size=8)
figrecrf, axesrecrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )
figrecd, axesrecd = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )


for i, (subtag, label) in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    a.plot_vs_count(f'{subtag}', 'rfs', marker='', linestyle='-',  fig=figrecrf, axes=axesrecrf,
                    color = cmap_rf[i], label=f'{label}',xlabel='Algorithm Iteration', ylabel='$R_f$',xerr=None,yerr=None)


    a.plot_vs_count(f'{subtag}', 'mean_dxyzs', marker='', linestyle='-', fig=figrecd, axes=axesrecd,
                    color =cmap_atomic[i], label=f'{label}',
                    ylabel='Mean Atomic Displacement', xlabel='Algorithm Iteration', logy=False, xerr=None, yerr=None)


axesrecrf.legend(loc="upper right", title='Iterative Scheme')
axesrecd.legend(loc="upper right", title='Iterative Scheme')
# axes[0].set_title('Iterative Algorithm Recipes')
axesrecrf.set_xlim(0.5, 120)
axesrecd.set_xlim(0.5, 120)
axesrecrf.set_ylim(0.145, 0.5)
axesrecd.set_ylim(0, 1.16)

figrecrf.tight_layout()
figrecd.tight_layout()
figrecrf.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_rec_rf.png')
figrecd.savefig('/home/pat/Documents/cloudstor/phd/writing/thesis/figs/py/iteralgo/algo_rec_d.png')



plt.show()

