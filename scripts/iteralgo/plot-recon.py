import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.close('all')



#### Define colors

blue = '#648FFF'
pink = '#DC267F'
orange = '#FE6100'

# fig, axes = plt.subplots(1,1)
# axes.plot([0, 0.0242], [0, 0.0242], color=(0,0,0), linestyle='dashed', label='y=x')

# a = scorpy.AlgoHandler('aluminophosphate-d05')
# print(a.tag)
# a.plot_intensity_xy('a', fig=fig, axes=axes, label='AlPO4', color=blue, marker='.', verbose=99)

# a = scorpy.AlgoHandler('tbcampmamp-d05')
# print(a.tag)
# a.plot_intensity_xy('a', fig=fig, axes=axes, label='C25H40N2O5', color=pink, marker='.', verbose=99)

# a = scorpy.AlgoHandler('agno3-d03')
# print(a.tag)
# a.plot_intensity_xy('a', fig=fig, axes=axes, label='AgNO3', color=orange, marker='.', verbose=99)
# plt.legend()
# plt.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/inten-xy.png')





capsize=2.5
errsf=3
fig, axes = plt.subplots(1,1)
axes.plot([1.45, 1.75], [1.45, 1.75], color=(0,0,0), linestyle='dashed', label='y=x')
a = scorpy.AlgoHandler('aluminophosphate-d07')
a.plot_bond_geometry_xy('a', fig=fig, axes=axes, marker='.', color=blue,capsize=capsize,errsf=errsf, verbose=99)
a.plot_bond_geometry_xy('b', fig=fig, axes=axes, marker='.', color=pink,capsize=capsize,errsf=errsf, verbose=99)
a.plot_bond_geometry_xy('c', fig=fig, axes=axes, marker='.', color=orange,capsize=capsize,errsf=errsf, verbose=99)



fig, axes = plt.subplots(1,1)
axes.plot([106, 150], [106, 150], color=(0,0,0), linestyle='dashed', label='y=x')
a = scorpy.AlgoHandler('aluminophosphate-d07')
a.plot_bond_geometry_xy('a',geometry='angles', fig=fig, axes=axes, marker='.', color=blue,capsize=capsize,errsf=errsf, verbose=99)
a.plot_bond_geometry_xy('b',geometry='angles', fig=fig, axes=axes, marker='.', color=pink,capsize=capsize,errsf=errsf, verbose=99)
a.plot_bond_geometry_xy('c',geometry='angles', fig=fig, axes=axes, marker='.', color=orange,capsize=capsize,errsf=errsf, verbose=99)



# fig, axes = plt.subplots(1,1)
# axes.plot([0, 0.0062], [0, 0.0062], color=(0,0,0), linestyle='dashed', label='y=x')
# a = scorpy.AlgoHandler('aluminophosphate-d07')
# a.plot_intensity_xy('a', n_scats=-1, fig=fig, axes=axes, marker='x', color=blue, verbose=99)
# a.plot_intensity_xy('b', n_scats=-1, fig=fig, axes=axes, marker='x', color=pink, verbose=99)
# a.plot_intensity_xy('c', n_scats=-1, fig=fig, axes=axes, marker='x', color=orange, verbose=99)






plt.show()




