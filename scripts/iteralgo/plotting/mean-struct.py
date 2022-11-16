
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.close('all')


import scorpy








# tag = 'agno3-d03'
tag = 'aluminophosphate-d05'

sub_tags = 'abcdefgh'






tag ='agno3-d03'

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

# print(d_std)
# print(a_std)

# print(d_mean)
# print(a_mean)


a_std = np.array([0.11010648, 0.07647508, 0.12871966, 0.4472136,  0.33797189, 0.38709656,
 0.16583124, 0.10098731, 0.15674422, 0.38058343, 0.34550687, 0.50744458,
 0.3199121,  0.34977671, 0.84963227, 0.66602834, 0.494343,   0.84557673,
 1.24874937, 0.7096434,  1.40334422, 1.54979837, 0.53851648, 1.14775596,
 0.22220486, 0.17853571, 0.24462982, 0.14086785, 0.32787193, 0.36314598,
 0.44440972,])

d_std = np.array( [0.0032572,  0.0043589,  0.00119,    0.00499844, 0.00330719, 0.00217586,
 0.01269843, 0.00496078, 0.00959736, 0.00657529, 0.00395087, 0.02107724,
 0.03218598, 0.02891258, 0.01719329, 0.00868548, 0.00408503, 0.00609816,
 0.00782524, 0.00379967,])


d_mean = np.array([2.273875,  2.51,      2.5044875, 2.569375,  1.80475,   1.846625,  1.28,
 1.266125,  1.241125,  1.346375,  1.366875,  1.3965,    1.26125,   1.44125,
 1.397875,  1.50475,   1.53325,   1.39975,   1.368625,  1.39975  ])

a_mean = np.array([ 94.02375, 132.59625, 132.6175,  125.5,      50.925,    95.9375,  102.45,
 108.18375, 112.0225,   93.8375,   97.025,   118.,      121.4375,  120.3625,
 121.325,   120.4875,  118.175,   122.4,     120.525,   120.5875,  117.575,
 120.525,   117.6,     121.8375,  112.775,   113.575,   119.7375,  118.4375,
 121.8,     119.275,   121.,     ])








fig, axes = plt.subplots(2,1,figsize=(7.87, 2*3.93), dpi=150 )

dtarg_vals, _ = a.get_geometry_vals('a', count='targ', geometry='distances')
dmean_vals, dmean_errs = a.get_geometry_vals('means', count=None, geometry='distances')

axes[0].plot([min(dmean_vals), max(dmean_vals)],[min(dmean_vals), max(dmean_vals)], linestyle='dotted')
a._plot_errorbar(dtarg_vals, dmean_vals, yerr=dmean_errs, fig=fig, axes=axes[0],
                 xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                marker=',', capsize=2)

a._plot_errorbar(dtarg_vals, d_mean, yerr=d_std, fig=fig, axes=axes[0], color='red',
                 xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                marker=',', capsize=2)


atarg_vals, _ = a.get_geometry_vals('a', count='targ', geometry='angles')
amean_vals, amean_errs = a.get_geometry_vals('means', count=None, geometry='angles')
axes[1].plot([min(amean_vals), max(amean_vals)],[min(amean_vals), max(amean_vals)], linestyle='dotted')
a._plot_errorbar(atarg_vals, amean_vals, yerr=amean_errs, fig=fig, axes=axes[1],
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker=',', capsize=2)

a._plot_errorbar(atarg_vals, a_mean, yerr=a_std, fig=fig, axes=axes[1], color='red',
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker=',', capsize=2)

plt.tight_layout()

# fig.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/bond-da-xy.png')

fig, axes = plt.subplots(2,1,figsize=(7.87, 2*3.93), dpi=150 )

derr2 = np.sqrt(dmean_errs**2 +d_std**2)
axes[0].plot([min(dmean_vals), max(dmean_vals)],[min(dmean_vals), max(dmean_vals)], linestyle='dotted')
a._plot_errorbar(dtarg_vals, dmean_vals, yerr=derr2*3, fig=fig, axes=axes[0],
                 xlabel='Target Bond Distance [\u212B]', ylabel='Recovered Bond Distance [\u212B]',
                marker='.', markersize=0.1, capsize=2)

aerr2 = np.sqrt(amean_errs**2 +a_std**2)
axes[1].plot([min(amean_vals), max(amean_vals)],[min(amean_vals), max(amean_vals)], linestyle='dotted')
a._plot_errorbar(atarg_vals, amean_vals, yerr=aerr2*3, fig=fig, axes=axes[1],
                 xlabel='Target Bond Angle [deg]', ylabel='Recovered Bond Angle [deg]',
                marker='.', markersize=0.1, capsize=2)


plt.tight_layout()




plt.show()






