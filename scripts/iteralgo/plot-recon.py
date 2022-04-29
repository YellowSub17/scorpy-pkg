import scorpy
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.cm as cm
plt.close('all')








tag = 'agno3-rec'

a = scorpy.AlgoHandler(tag)
sub_tags = ['ER120', 'HIO10ER10', 'HIO20ER20', 'HIO30ER30', 'HIO60ER60', 'HIO120', 'HIO120beta']
colors = cm.tab10(np.linspace(0, 1, len(sub_tags)))


fig, axes = plt.subplots(1,1)
for sub_tag, color in zip(sub_tags, colors):
    a.plot_rfs(sub_tag, calc='shelx', label=sub_tag, fig=fig, axes=axes, color=color, marker='', linestyle='solid')
axes.set_title(f'{a.tag} - Shelx')
plt.legend()

fig, axes = plt.subplots(1,1)
for sub_tag, color in zip(sub_tags, colors):
    a.plot_rfs(sub_tag, calc='inten', label=sub_tag, fig=fig, axes=axes, color=color, marker='', linestyle='solid')
axes.set_title(f'{a.tag} - Inten')
plt.legend()







nqs = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250]

colors = cm.tab10(np.linspace(0, 1, len(nqs)))

fig, axes = plt.subplots(1,1)
for nq, color in zip(nqs, colors):


    if nq==150:
        tag = 'agno3-nl180'
    elif nq==200:
        tag = 'agno3-random-starts'
    else:
        tag = f'agno3-nq{nq}'


    a = scorpy.AlgoHandler(tag)

    a.plot_rfs('a', calc='shelx', label=f'{nq}', fig=fig, axes=axes, color=color, marker='', linestyle='solid')

plt.legend()
axes.set_title(f'nq - Shelx')





fig, axes = plt.subplots(1,1)
for nq, color in zip(nqs, colors):


    if nq==150:
        tag = 'agno3-nl180'
    elif nq==200:
        tag = 'agno3-random-starts'
    else:
        tag = f'agno3-nq{nq}'


    a = scorpy.AlgoHandler(tag)

    a.plot_rfs('a', calc='inten', label=f'{nq}', fig=fig, axes=axes, color=color, marker='', linestyle='solid')

plt.legend()
axes.set_title(f'nq - Inten')






a = scorpy.AlgoHandler('agno3-nq125')

a.intensity_xy_plot('a')
a.bond_distances_xy_plot('a')
a.bond_angles_xy_plot('a')
















plt.show()




