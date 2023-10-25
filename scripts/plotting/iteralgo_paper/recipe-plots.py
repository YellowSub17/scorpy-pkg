
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np





subtags = [('ER120','120ER'),
           ('HIO10ER10','(10HIO+10ER)x12'),
           ('HIO20ER20','(20HIO+20ER)x6'),
           ('HIO30ER30','(30HIO+30ER)x3'),
           ('HIO120','120HIO'),
           ('a','(20HIO+2ER)x5')
           ]




cmap_rf = cm.winter( np.linspace(0, 1, len(subtags)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(subtags)))



plt.rc('font', size=8)
figrecrf, axesrecrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )
figrecd, axesrecd = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )



for i, (subtag, label) in enumerate(subtags):
    a = scorpy.AlgoHandler('agno3-rec')
    iter_counts = [i for i in range(121)]
    if subtag=='a':
        a = scorpy.AlgoHandler('agno3-nl180')
        iter_counts = [i for i in range(111)]

    # a.plot_vs_count(f'{subtag}', 'rfs', marker='', linestyle='-',  fig=figrecrf, axes=axesrecrf,
                    # color = cmap_rf[i], label=f'{label}',xlabel='Algorithm Iteration', ylabel='$R_f$',xerr=None,yerr=None)

    It = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-targ.npy')
    loc = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-It-If-loc.npy')

    It = It/np.sum(It)
    If = a.get_inten_quick(subtag, iter_counts, loc)

    If = If/np.sum(If, axis=-1)[:,None]

    rfs = np.sum(np.abs(It - If), axis=-1) /np.sum( np.abs(If), axis=-1 )

    axesrecrf.plot(iter_counts, rfs, marker=',', linestyle='-', color=cmap_rf[i], label=f'{label}')
    # axesnlrf.plot(iter_counts, np.log10(rfs), marker=',', linestyle='-', color=cmap_rf[i], label=f'{nl}')
    axesrecrf.set_ylabel('Crystallographic $R$ Factor')
    axesrecrf.set_xlabel('Algorithm Iteration')





    a.plot_vs_count(f'{subtag}', 'mean_dxyzs', marker='', linestyle='-', fig=figrecd, axes=axesrecd,
                    color =cmap_atomic[i], label=f'{label}',
                    ylabel='Mean Atomic Displacement', xlabel='Algorithm Iteration', logy=False, xerr=None, yerr=None)


axesrecrf.legend(loc="upper right", title='Iterative Scheme:', frameon=False)
axesrecd.legend(loc="upper right", title='Iterative Scheme:', frameon=False)
# axes[0].set_title('Iterative Algorithm Recipes')
axesrecrf.set_xlim(0, 120)
axesrecrf.set_ylim(0, 1.2)

axesrecd.set_xlim(0, 120)
axesrecd.set_ylim(0, 1.16)

figrecrf.tight_layout()
figrecd.tight_layout()
figrecrf.savefig('/home/pat/Documents/phd/figs/py/algo_rec_rf.svg')
figrecd.savefig('/home/pat/Documents/phd/figs/py/algo_rec_d.svg')



plt.show()

