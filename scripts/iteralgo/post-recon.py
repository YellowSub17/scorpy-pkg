#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import time
import os
plt.close('all')








a = scorpy.AlgoHandler('agno3-rec')

sub_tags = ['ER120', 'HIO10ER10', 'HIO20ER20', 'HIO30ER30', 'HIO60ER60', 'HIO120', 'HIO120beta']
counts = [i for i in range(121)]



for sub_tag in sub_tags:

    a.run_shelx(sub_tag)
    a.run_shelx(sub_tag, count='targ')

    for count in counts:
        print(sub_tag, count)
        a.run_shelx(sub_tag, count=count)




for sub_tag in sub_tags:

    a.save_rfs(sub_tag, verbose=99)





# nqs = [25, 50, 75, 100, 125, 175, 225, 250]
# colors = cm.jet(np.linspace(0, 1, len(nqs)))

# fig, axes = plt.subplots(1,1)
# for nq, col in zip(nqs, colors):
    # a = scorpy.AlgoHandler(f'agno3-nq{nq}')







    # a.plot_rfs('a', calc='shelx', fig=fig, axes=axes, color=col, marker='.', label=f'{nq}-s')
    # a.plot_rfs('a', calc='inten', fig=fig, axes=axes, color=col, marker='x', label=f'{nq}-i')
# plt.legend()

# plt.show()












