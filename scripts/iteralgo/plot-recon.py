import scorpy
import numpy as np
import matplotlib.pyplot as plt

import matplotlib.cm as cm
plt.close('all')








# tag = 'agno3-rec'

# a = scorpy.AlgoHandler(tag)
# sub_tags = ['ER120', 'HIO10ER10', 'HIO30ER30', 'HIO120']

# colors = [ (1,0,0), (0.25, 0.75, 0.25), (0,0,1), (0.95, 0.45, 0.15)]

# fig, axes = plt.subplots(1,1)
# for sub_tag, color in zip(sub_tags, colors):
    # a.plot_rfs(sub_tag, calc='shelx', label=sub_tag, fig=fig, axes=axes, color=color,
                        # xlabel='Iteration Number', ylabel='$R_f$', title='Algorithm Recipe',
                        # marker='', linestyle='solid')
# plt.legend()
# plt.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/recipes.png')




a = scorpy.AlgoHandler('agno3-d03')
fig, axes = plt.subplots(1,1)
a.plot_intensity_xy('a', color_by=('theta', 'jet'),n_intens=10, fig=fig, axes=axes, verbose=99)
# a.plot_intensity_xy('a', color=np.array([0.1,0.2,0.6]))




# elinewidth=0.5
# capsize=0.0




# fig, axes = plt.subplots(1,1)
# a = scorpy.AlgoHandler('agno3-d03')
# a.plot_mean_dgeom('a', fig=fig, axes=axes, color=(0.2,0.7,0.2), count_max=110, elinewidth=elinewidth, capsize=capsize)
# a = scorpy.AlgoHandler('agno3-nq250')
# a.plot_mean_dgeom('a', fig=fig, axes=axes, color=(0,0,1), count_max=110, dx=0.6, elinewidth=elinewidth, capsize=capsize)

# a = scorpy.AlgoHandler('agno3-nq75')
# a.plot_mean_dgeom('a', fig=fig, axes=axes, color=(1,0,0), count_max=110, dx=0.3, elinewidth=elinewidth, capsize=capsize)


# fig, axes = plt.subplots(1,1)
# a = scorpy.AlgoHandler('agno3-d03')
# a.plot_mean_dgeom('a', geometry='angle', fig=fig, axes=axes, color=(0.2,0.7,0.2), count_max=110, elinewidth=elinewidth, capsize=capsize)
# a = scorpy.AlgoHandler('agno3-nq250')
# a.plot_mean_dgeom('a', geometry='angle', fig=fig, axes=axes, color=(0,0,1), count_max=110, dx=0.6, elinewidth=elinewidth, capsize=capsize)

# a = scorpy.AlgoHandler('agno3-nq75')
# a.plot_mean_dgeom('a', geometry='angle', fig=fig, axes=axes, color=(1,0,0), count_max=110, dx=0.3, elinewidth=elinewidth, capsize=capsize)





# fig, axes = plt.subplots(1,1)
# a = scorpy.AlgoHandler('agno3-d05')
# a.plot_mean_dgeom('a',geometry='angle', fig=fig, axes=axes, color=(1,0,0))

# a = scorpy.AlgoHandler('agno3-d03')
# a.plot_mean_dgeom('a',geometry='angle', fig=fig, axes=axes, color=(0.2,0.7,0.2),dx=0.1)

# a = scorpy.AlgoHandler('agno3-nq250')
# a.plot_mean_dgeom('a',geometry='angle', fig=fig, axes=axes, color=(0,0,1),dx=0.2)









# nqs = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250,]

# colors = cm.jet(np.linspace(0, 1, len(nqs)))

# fig, axes = plt.subplots(1,1)
# for nq, color in zip(nqs, colors):


    # if nq==150:
        # tag = 'agno3-nl180'
    # elif nq==200:
        # tag = 'agno3-random-starts'
    # elif nq==3:
        # tag = 'agno3-d03'
    # elif nq==5:
        # tag = 'agno3-d05'
    # else:
        # tag = f'agno3-nq{nq}'


    # a = scorpy.AlgoHandler(tag)

    # a.plot_rfs('a', calc='shelx', label=f'{nq}', fig=fig, axes=axes, color=color,
                # xlabel='Iteration Number', ylabel='$R_f$', title='Radial $q$ Sampling',
                # marker='', linestyle='solid')


# plt.legend()

# plt.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nqsampling.png')






# nls = [i for i in range(60, 181, 15)]
# colors = cm.jet(np.linspace(0, 1, len(nls)))
# fig, axes = plt.subplots(1,1)

# for nl, color in zip(nls, colors):

    # a = scorpy.AlgoHandler(f'agno3-nl{nl}')

    # a.plot_rfs('a', calc='shelx', label=f'{nl}', fig=fig, axes=axes, color=color,
                # xlabel='Iteration Number', ylabel='$R_f$', title='Angular nL Sampling',
                # marker='', linestyle='solid')
# plt.legend()
# plt.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nlsampling.png')




# # # nqs = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250,]
# # # nqs = [50, 100, 150,  200,  250]
# # nqs = [25, 50, 75, 100, 125, 150, 175, 200, 225, 250,]
# # colors = cm.tab10(np.linspace(0, 1, len(nqs)))

# # fig, axes = plt.subplots(1,1)
# # for nq, color in zip(nqs, colors):


    # # if nq==150:
        # # tag = 'agno3-nl180'
    # # elif nq==200:
        # # tag = 'agno3-random-starts'
    # # elif nq==3:
        # # tag = 'agno3-d03'
    # # elif nq==5:
        # # tag = 'agno3-d05'
    # # else:
        # # tag = f'agno3-nq{nq}'


    # # a = scorpy.AlgoHandler(tag)

    # # a.plot_mean_dgeom('a', calc='shelx', label=f'{nq}', geometry='distances', fig=fig, axes=axes, color=color, marker='', linestyle='solid')

# # plt.legend()
# # axes.set_title(f'mean dBondDistance')














plt.show()




