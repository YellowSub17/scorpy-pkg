import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.rc('font', size=8)
import scorpy
from mpl_toolkits.axes_grid.inset_locator import (inset_axes, InsetPosition, mark_inset)




# # a = scorpy.AlgoHandler('agno3-d07')
# a = scorpy.AlgoHandler('agno3-nl180')
# It, If = a.get_intensity('a')

# for count in [1, 10]:
    # print(f'{count=}')

    # Ifs = np.zeros((4, np.shape(It)[0]))

    # for i, subtag in enumerate('abcd'):

        # print(subtag)
        # _, If_subtag = a.get_intensity(subtag, count=count)

        # Ifs[i,:] =  If_subtag



    # If_mean = np.mean(Ifs, axis=0)
    # If_std = np.std(Ifs, axis=0)



    # np.save(f'/home/pat/Desktop/agno3-nl180-inten-mean_{count}.npy', If_mean)
    # np.save(f'/home/pat/Desktop/agno3-nl180-inten-std_{count}.npy', If_std)



a = scorpy.AlgoHandler('agno3-nl180')
It, If = a.get_intensity('a')



i_s = [1, 15,  30, 60, 90]
# colors = ['y', 'g', 'c', 'b', 'm']

al= 1
colors = [  (198/256, 185/256, 33/256, al),
            (85/256, 163/256, 26/256, al),
            (91/256, 234/256, 227/256, al),
            (37/256, 26/256, 244/256, al),
            (237/256, 26/256, 244/256, al),
         ]

# markers = [ "h", 's', 'X', "D", '.' ]
# markers = ['.', '.', '.', 'D', '.',]

markers = [ 'H', 'h', 's', 'D', '.']

          # 'g', 'c', 'b', 'm']
# colors = cm.hsv( np.linspace(0.1, 0.8, len(i_s)))

xy = np.linspace(0, 1)

# for i, (count, color) in enumerate(zip(i_s, colors)):
    
    # It = It[:2000]
    # If_mean = np.load(f'/home/pat/Desktop/agno3-nl180-inten-mean_{count}.npy')[:2000]
    # If_std = np.load(f'/home/pat/Desktop/agno3-nl180-inten-std_{count}.npy')[:2000]


    # fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )

    # plt.plot(xy,xy, 'k-.')

    # It_max_loc = np.where(It==np.max(It))


    # axes.plot(It/It[It_max_loc], If_mean/If_mean[It_max_loc],
              # ls='', marker='.',  color=color, markersize=3)

    
    # axes.set_xlim([-0.0125,1.0125])
    # # axes.set_ylim([-0.1, np.max(If_mean)/If_mean[It_max_loc]])



fig, axes = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True)

# inset_axes0 = plt.axes()
# inset_axes0.get_xaxis().set_visible(True)
# inset_axes0.get_yaxis().set_visible(True)
# ip0 = InsetPosition(axes, [0.45, 0.65, 0.525, 0.325])
# inset_axes0.set_axes_locator(ip0)
# mark_inset(axes, inset_axes0, loc1=3, loc2=4, fc='0.75', ec='none')


# axes.set_facecolor('black')
for i, (count, color, marker) in enumerate(zip(i_s, colors, markers)):

    It = It[:1000]
    If_mean = np.load(f'/home/pat/Desktop/agno3-nl180-inten-mean_{count}.npy')[:1000]
    If_std = np.load(f'/home/pat/Desktop/agno3-nl180-inten-std_{count}.npy')[:1000]
    It_max_loc = np.where(It==np.max(It))


    # axes.errorbar(It/np.max(It), If_mean/np.max(If_mean), If_std/np.max(If_mean), fmt='.', markersize=3, ls='', color=cmap[i])

    # axes.plot(It/It[It_max_loc], If_mean/If_mean[It_max_loc],
              # ls='', marker=marker,  color=color, markersize=2, label=f'{count}')

    axes.plot(It/np.sum(It)*100, If_mean/np.sum(If_mean)*100,
              ls='', marker=marker,  color=color, markersize=2, label=f'{count}')

    axes.set_xlim([-0.01, 0.83])
    axes.set_ylim([-0.01, 0.83])

#     inset_axes0.plot(It/It[It_max_loc], If_mean/If_mean[It_max_loc],
              # ls='', marker=marker,  color=color, markersize=1)

    # inset_axes0.set_xlim([-0.005, 0.1])
    # inset_axes0.set_ylim([-0.005, 0.1])

    # inset_axes0.set_xticks([0.01, 0.075])
    # inset_axes0.set_yticks([0.01, 0.075])




plt.plot(xy,xy, 'k-.', label='y=x')

axes.set_xlabel('Normalized Target Intensity [A.U]')
axes.set_ylabel('Normalized Recovered Intensity [A.U]')
axes.legend(bbox_to_anchor=(0,1), loc="upper left", framealpha=1, title='Iteration Number', ncol=2,)
    # borderpad=0.5,
    # labelspacing=0,
    # handlelength=0,
    # handletextpad=0.5,
    # columnspacing=1.5
              # )
plt.tight_layout()


fig.savefig('/home/pat/Documents/phd/writing/iteralgopaper/figs/py/intensity_xy.png')



plt.show()




