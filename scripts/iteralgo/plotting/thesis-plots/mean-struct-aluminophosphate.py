
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.close('all')


import scorpy

from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)








tag = 'aluminophosphate-d05'

sub_tags = 'abcdefgh'




a = scorpy.AlgoHandler(tag)


# sub_dvals = []
# sub_avals = []

# for subtag in 'abcdefgh':
    # print(subtag)
    # d_vals, _ = a.get_geometry_vals(subtag, count=None, geometry='distances')
    # a_vals, _ = a.get_geometry_vals(subtag, count=None, geometry='angles')
    # sub_dvals.append(d_vals)
    # sub_avals.append(a_vals)


# d_mean = np.array(sub_dvals).mean(axis=0)
# a_mean = np.array(sub_avals).mean(axis=0)
# d_std = np.array(sub_dvals).std(axis=0)
# a_std = np.array(sub_avals).std(axis=0)

# print(a_std)
# print(d_std)

# print(a_mean)
# print(d_mean)




#### Errors and mean across individual iterations

a_std = np.array([0.31795243, 0.2471715,  0.21794495, 0.17853571, 0.07372881, 0.23684119,
 0.28173569, 0.3391165,  0.16583124, 0.34550687, 0.21758619, 0.13973189,
 0.16533583, 0.18060662, 0.12267844, 0.19117646, 0.12868931, 0.18223868,
 0.29341736, 0.17139137, 0.34278273, 0.23418742, 1.83162326, 2.32580631,
 4.68874983, 4.26468053, 2.90473751,]  )

d_std = np.array([0.00632332, 0.00355097, 0.0035,     0.00289126, 0.00729619, 0.00576086,
 0.00324037, 0.0034187,  0.00502338, 0.00360555, 0.00446514, 0.00269258,
 0.01449784, 0.01932453, 0.04924429, 0.04106017, 0.0939082,  0.04062019])

d_mean = np.array([111.0875,  111.8875,  107.75,    109.625,   109.15875, 107.2125,  109.975,
 112.05,    108.85,    108.325,   109.8625,  107.69,    108.85125, 106.3975,
 110.415,   111.26375, 109.96875, 109.89125, 149.8875,  139.575,   146.3,
 142.0375,  115.2625,  117.925,   128.375,   110.75,    111.75,   ])

a_mean = np.array([1.498375, 1.523125, 1.533,    1.547875, 1.496375, 1.52675,  1.522,    1.54475,
 1.734375, 1.731,    1.73825,  1.7375,   1.46925,  1.53375,  1.575,    1.55125,
 1.4125,   1.485,   ])



#### Target distance and angles
dtarg_vals, dtarg_err = a.get_geometry_vals('a', count='targ', geometry='distances')
atarg_vals, atarg_err = a.get_geometry_vals('a', count='targ', geometry='angles')


#### bond distances and angles after averaging intenisty across runs
dmeans_vals, dmeans_errs = a.get_geometry_vals('means', count=None, geometry='distances')
ameans_vals, ameans_errs = a.get_geometry_vals('means', count=None, geometry='angles')


d_totalerr = np.sqrt(dmeans_errs**2 +d_std**2)
a_totalerr = np.sqrt(ameans_errs**2 +a_std**2)

# d_totalerr = dmeans_errs
# a_totalerr = ameans_errs

# d_totalerr = d_std
# a_totalerr = a_std







fig, axes = plt.subplots(2,1,figsize=(7.87, 2*3.93), dpi=150 )

axes[0].plot([min(dmeans_vals), max(dmeans_vals)],[min(dmeans_vals), max(dmeans_vals)], linestyle='dotted')
axes[1].plot([min(ameans_vals), max(ameans_vals)],[min(ameans_vals), max(ameans_vals)], linestyle='dotted')


a._plot_errorbar(dtarg_vals, dmeans_vals, yerr=d_totalerr*3, xerr=dtarg_err*0, fig=fig, axes=axes[0],
                 xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                marker='.', markersize=3, capsize=2, color='black')
a._plot_errorbar(atarg_vals, ameans_vals, yerr=a_totalerr*3, xerr=atarg_err*0, fig=fig, axes=axes[1],
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker='.', markersize=3, capsize=2, color='black')




# inset_axes0 = plt.axes()
# inset_axes0.get_xaxis().set_visible(False)
# inset_axes0.get_yaxis().set_visible(False)
# ip0 = InsetPosition(axes[0], [0.01, 0.55, 0.45, 0.425])
# inset_axes0.set_axes_locator(ip0)
# mark_inset(axes[0], inset_axes0, loc1=3, loc2=4, fc='none', ec='black')

# inset_axes0.plot([min(dmeans_vals), max(dmeans_vals)],[min(dmeans_vals), max(dmeans_vals)], linestyle='dotted')
# a._plot_errorbar(dtarg_vals, dmeans_vals, yerr=d_totalerr*3, xerr=dtarg_err*0, fig=fig, axes=inset_axes0,
                 # xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                # marker='.', markersize=3, capsize=2)


# inset_axes0.set_xlim([1.2205,1.445])
# inset_axes0.set_ylim([1.088,1.61975])








inset_axes1 = plt.axes()
inset_axes1.get_xaxis().set_visible(False)
inset_axes1.get_yaxis().set_visible(False)
ip1 = InsetPosition(axes[1], [0.5, 0.01, 0.49, 0.425])
inset_axes1.set_axes_locator(ip1)
mark_inset(axes[1], inset_axes1, loc1=2, loc2=3, fc='0.75', ec='none')
inset_axes1.plot([min(ameans_vals), max(ameans_vals)],[min(ameans_vals), max(ameans_vals)], linestyle='dotted')

a._plot_errorbar(atarg_vals, ameans_vals, yerr=a_totalerr*3, xerr=atarg_err*0, fig=fig, axes=inset_axes1,
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker='.', markersize=3, capsize=2)

inset_axes1.set_xlim([106.24822, 111.9820])
inset_axes1.set_ylim([104.5701, 114.122])


plt.tight_layout()


fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/bond-da-xy-aluminophosphate.png')


plt.show()






