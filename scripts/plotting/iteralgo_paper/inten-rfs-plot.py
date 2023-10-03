import scorpy
import matplotlib.pyplot as plt
import numpy as np

import matplotlib.cm as cm
plt.close('all')
plt.rc('font', size=8)
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)






tag = 'tbcampmamp-d05'
subtags = 'abcdefgh'
# subtags = 'abc'
loc = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-It-If-loc.npy')
a = scorpy.AlgoHandler(tag)
iter_counts = [i for i in range(121)]

# It = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-targ.npy')
# Its, _ = np.meshgrid(It/np.sum(It), iter_counts)
# rfs = np.zeros((len(iter_counts), len(subtags)))
# for i, subtag in enumerate(subtags):
    # print(f'{subtag=}')
    # # Ifs = a.get_inten_quick(subtag, counts=iter_counts, loc=loc)
    # # np.save(f'/media/pat/datadrive/other-algo-crap/{tag}-Ifs-{subtag}.npy', Ifs)

    # Ifs = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-Ifs-{subtag}.npy')
    # Ifs = Ifs/np.sum(Ifs, axis=-1)[:,None]
    # rfs[:, i] = np.sum(np.abs(Its - Ifs), axis=-1) /np.sum( np.abs(Ifs), axis=-1 )

# np.save(f'/media/pat/datadrive/other-algo-crap/{tag}-rfs.npy', rfs)






fig, axes = plt.subplots(1,3,figsize=(16/2.54, 8/2.54), dpi=300, sharex=True, sharey=True )

tags = ['agno3-d03', 'aluminophosphate-d05', 'tbcampmamp-d05']
labels= ['Silver Nitrate/Ligand', 'Aluminophosphate', 'Dipeptide Precursor']
# labels= ['AgNO$_3$', 'AlPO$_4$', 'C$_{25}$H$_{40}$N$_2$O$_5$']
colors ='rgb'
for tag, color, label, ax in zip(tags, colors, labels, axes.flatten()):
    rfs = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-rfs.npy')

    rfs_means = np.mean(rfs, axis=-1)
    rfs_std = np.std(rfs, axis=-1)

    bounds_xpts = iter_counts+iter_counts[::-1]

    std_f = 3
    bounds_ypts = list(rfs_means+std_f*rfs_std)+ list(rfs_means[::-1]-std_f*rfs_std[::-1])


    ax.fill(bounds_xpts, bounds_ypts, color=color, alpha=0.3)
    ax.plot(iter_counts, rfs_means, color=color, linewidth=1, label=label)
    ax.text(115, 1.1, f'{label}', ha='right')

    ax.set_xlim([0, 120])
    ax.set_ylim([0.0, 1.20])
    ax.set_xticks([0, 30,  60, 90, 120])
    ax.set_yticks(np.linspace(0, 1.2, 7))


# axes.legend(loc='lower left', ncol=1, frameon=False)

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)

plt.ylabel('R$_f$')
plt.xlabel('Algorithm Iteration')


plt.subplots_adjust(top=0.95,
bottom=0.15,
left=0.1,
right=0.95,
hspace=0.2,
wspace=0.15)




plt.savefig(f'/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_rfs_1x3.png')







# fig, axes = plt.subplots(1,1,figsize=(16/2.54, 8/2.54), dpi=300 )

# inset_axes0 = plt.axes()
# inset_axes0.get_xaxis().set_visible(True)
# inset_axes0.get_yaxis().set_visible(True)

# ip0 = InsetPosition(axes, [0.55, 0.55, 0.425, 0.425])
# inset_axes0.set_axes_locator(ip0)
# mark_inset(axes, inset_axes0, loc1=3, loc2=4, fc='0.75', ec='none')


# tags = ['agno3-d03', 'aluminophosphate-d05', 'tbcampmamp-d05']
# # labels= ['Silver Nitrate', 'Aluminophosphate', 'Dipeptide Precursor']
# labels= ['AgNO$_3$', 'AlPO$_4$', 'C$_{25}$H$_{40}$N$_2$O$_5$']
# colors ='rgb'
# for tag, color, label in zip(tags, colors, labels):
    # rfs = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-rfs.npy')

    # rfs_means = np.mean(rfs, axis=-1)
    # rfs_std = np.std(rfs, axis=-1)

    # bounds_xpts = iter_counts+iter_counts[::-1]

    # std_f = 3
    # bounds_ypts = list(rfs_means+std_f*rfs_std)+ list(rfs_means[::-1]-std_f*rfs_std[::-1])


    # for a in [axes, inset_axes0]:
        # a.fill(bounds_xpts, bounds_ypts, color=color, alpha=0.3)
        # a.plot(iter_counts, rfs_means, color=color, linewidth=1, label=label)

# axes.set_xlim([0, 120])
# axes.set_ylim([0.0, 1.20])
# axes.set_xticks([0, 30,  60, 90, 120])
# axes.set_yticks(np.linspace(0, 1.2, 7))

# inset_axes0.set_xlim([55, 120])
# inset_axes0.set_ylim([0.14, 0.3])

# axes.legend(loc='lower left', ncol=1, frameon=False)
# axes.set_xlabel('Algorithm Iteration')
# axes.set_ylabel('R$_f$')
# plt.tight_layout()




































plt.show()

