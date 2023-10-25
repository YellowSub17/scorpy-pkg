
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.close('all')


import scorpy




import mpl_toolkits
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)





plt.rc('font', size=8)



tag = 'tbcampmamp-d05'

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

# print('a_std=np.array(',a_std,')')
# print('d_std=np.array(',d_std,')')


# print('a_mean=np.array(',a_mean,')')
# print('d_mean=np.array(',d_mean,')')




#### Errors and mean across individual iterations

a_std=np.array( [0.21650635, 0.17320508, 0.12183493, 0.11659224, 0.14947826, 0.24462982,
 0.25708705, 0.349106,   0.30413813, 0.27838822, 0.40543187, 0.41758233,
 0.18328598, 0.39051248, 0.33166248, 0.20577597, 0.19960899, 0.09921567,
 0.14523688, 0.17984368, 0.17984368, 0.30593096, 0.44440972, 0.52186564,
 0.51720402, 0.17275344, 0.21065374, 0.12990381, 0.19364917, 0.2,
 0.19960899, 0.20271593, 0.31622777, 0.71490821, 0.2727178,  0.26190409,
 0.1763342,  0.13919411, 0.27128168, 0.28284271, 0.3854786,  0.30998992,
 0.56513273, 0.44982636] )
d_std=np.array( [0.00234521, 0.00268095, 0.00351559, 0.00342555, 0.00252178, 0.00147902,
 0.00313996, 0.00367211, 0.00395087, 0.00289126, 0.00307205, 0.00121835,
 0.00363791, 0.00380789, 0.0054872,  0.00626498, 0.009701,   0.00809224,
 0.00924662, 0.00263391, 0.00405432, 0.00441411, 0.00909584, 0.00580948,
 0.00286956, 0.00494343, 0.0040601,  0.01874125, 0.00961769, 0.00538516,
 0.00722734, 0.00696419] )
a_mean=np.array( [114.775,  120.45,   124.2375, 119.2125, 116.0375, 117.9625, 118.7875, 122.175,
 119.05,   121.5,    119.275,  120.325,  119.8875, 120.15,   107.4,    124.8375,
 125.8375, 109.2375, 107.6125, 113.0375, 111.2375, 115.0875, 114.15,   110.2375,
 109.2,    121.8625, 119.975,  118.075,  109.9,    110.95,   107.6375, 115.8875,
 109.,     113.4125, 110.825,  126.0125, 122.9125, 111.025,  110.2125, 109.2,
 112.3875, 102.4875, 110.225,  111.8375] )
d_mean=np.array( [1.3385,   1.46025,  1.190125, 1.224625, 1.204875, 1.34375,  1.478875, 1.354625,
 1.480125, 1.464125, 1.37225,  1.437375, 1.398625, 1.385,    1.477875, 1.3625,
 1.388125, 1.386375, 1.3855,   1.52875,  1.53375,  1.530625, 1.509375, 1.5345,
 1.528375, 1.54025,  1.523375, 1.476625, 1.513,    1.5025,   1.524375, 1.507,   ] )

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







fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )

axes.plot([min(dmeans_vals), max(dmeans_vals)],[min(dmeans_vals), max(dmeans_vals)], linestyle='dotted')


a._plot_errorbar(dtarg_vals, dmeans_vals, yerr=d_totalerr*3, xerr=dtarg_err*0, fig=fig, axes=axes,
                 xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                marker='.', markersize=3, capsize=2, color=(0.5,0.5,0.5), ecolor='black')

plt.tight_layout()
fig.savefig('/home/pat/Documents/phd/figs/py/algo_tbcampmamp_lengths.svg')


fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300 )
axes.plot([min(ameans_vals), max(ameans_vals)],[min(ameans_vals), max(ameans_vals)], linestyle='dotted')
a._plot_errorbar(atarg_vals, ameans_vals, yerr=a_totalerr*3, xerr=atarg_err*0, fig=fig, axes=axes,
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker='.', markersize=3, capsize=2,color=(0.5,0.5,0.5), ecolor='black')


plt.tight_layout()
fig.savefig('/home/pat/Documents/phd/figs/py/algo_tbcampmamp_angles.svg')




plt.show()






