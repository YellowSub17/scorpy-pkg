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




# fig, axes = plt.subplots(1,1)
# axes.plot([0, 1], [0, 1], 'k-')
# a = scorpy.AlgoHandler('agno3-nq25')
# a.plot_intensity_xy('a', color=(0.3,0.8,0.3), n_scats=5000, fig=fig, axes=axes, verbose=99)

# a = scorpy.AlgoHandler('agno3-nq50')
# a.plot_intensity_xy('a', color=(0,0,1), n_scats=5000, fig=fig, axes=axes, verbose=99)

# a = scorpy.AlgoHandler('agno3-nq75')
# a.plot_intensity_xy('a', color=(1,0,0), n_scats=5000, fig=fig, axes=axes, verbose=99)

# a = scorpy.AlgoHandler('agno3-nq250')
# a.plot_intensity_xy('a', color=(1,0.5,0.1), n_scats=5000, fig=fig, axes=axes, verbose=99)





elinewidth=1.0
capsize=0.5
marker=','




fig, axes = plt.subplots(1,1)
a = scorpy.AlgoHandler('agno3-nq250')
a.plot_mean_dgeom('a', fig=fig, axes=axes, color=(0,0,1), count_max=110,
                  ylabel='Average Difference in Bond Length [A]', xlabel='Iteration Number',
                  elinewidth=elinewidth, capsize=capsize, marker=marker, label='d07')
a = scorpy.AlgoHandler('agno3-d03')
a.plot_mean_dgeom('a', fig=fig, axes=axes, color=(1,0,0), count_max=110, dx=0.5,
                  ylabel='Average Difference in Bond Length [A]', xlabel='Iteration Number',
                  elinewidth=elinewidth, capsize=capsize,marker=marker, label='d03')
plt.legend()






fig, axes = plt.subplots(1,1)

a = scorpy.AlgoHandler('agno3-nq250')
a.plot_mean_dgeom('a', geometry='angle', fig=fig, axes=axes, color=(0,0,1), count_max=110,
                  ylabel='Average Difference in Bond Angle [deg]', xlabel='Iteration Number',
                  elinewidth=elinewidth, capsize=capsize, marker=marker, label='d07')

a = scorpy.AlgoHandler('agno3-d03')
a.plot_mean_dgeom('a', geometry='angle', fig=fig, axes=axes, color=(1,0,0), count_max=110, dx=0.5,
                  ylabel='Average Difference in Bond Angle [deg]', xlabel='Iteration Number',
                  elinewidth=elinewidth, capsize=capsize, marker=marker, label='d03')

plt.legend()





# nqs = [25, 50, 75, 250,]

# colors = [(0.3,0.8,0.3),(0,0,1),(1,0,0),(1,0.5,0.1)]



# fig, axes = plt.subplots(1,1)
# for nq in [100, 125, 150, 175, 200, 225]:
    # if nq==150:
        # tag = 'agno3-nl180'
    # elif nq==200:
        # tag = 'agno3-random-starts'
    # else:
        # tag = f'agno3-nq{nq}'

    # a = scorpy.AlgoHandler(tag)
    # a.plot_rfs('a', calc='shelx', fig=fig, axes=axes, color=(0.5,0.5,0.5),
                # xlabel='Iteration Number', ylabel='$R_f$',
                # marker='', linestyle='dashed')
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



    # a.plot_rfs('a', calc='shelx', label=f'nq={nq}', fig=fig, axes=axes, color=color,
                # xlabel='Iteration Number', ylabel='$R_f$',
                # marker='', linestyle='solid')


# plt.legend()

# plt.savefig('/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/nqsampling.png')





# a = scorpy.AlgoHandler('agno3-d03')
# a.plot_rfs('a')




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













plt.show()




