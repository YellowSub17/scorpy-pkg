import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
plt.close('all')
plt.rc('font', size=8)
import scorpy


import mpl_toolkits
from mpl_toolkits.axes_grid1.inset_locator import (inset_axes, InsetPosition, mark_inset)



# ######GET LOCS
# # tags = ['tbcampmamp-d07','tbcampmamp-d05', 'aluminophosphate-d07', 'aluminophosphate-d07' ]
# tags = ['agno3-d05' ]
# subtag = 'a'

# for tag in tags:
    # a = scorpy.AlgoHandler(tag)
    # print('getting loc')
    # loc = a.get_It_If_loc(subtag)
    # np.save(f'/media/pat/datadrive/other-algo-crap/{tag}-It-If-loc.npy', loc)



    # a = scorpy.AlgoHandler(tag)
    # print('saving target inten')
    # It = a.get_targ_inten()
    # np.save(f'/media/pat/datadrive/other-algo-crap/{tag}-targ.npy', It)


# #####CALC MEANS
# tag = 'agno3-d05'
# subtags = 'abcdefgh'
# # subtags = 'abc'
# loc = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-It-If-loc.npy')
# a = scorpy.AlgoHandler(tag)

# iter_counts = [i for i in range(121)]

# It = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-targ.npy')

# Ifs_all_subtags = np.zeros( (len(iter_counts), It.shape[0], len(subtags)) )


# for i, subtag in enumerate(subtags):
    # print(subtag)
    # Ifs = a.get_inten_quick(subtag, counts=iter_counts, loc=loc)
    # Ifs_all_subtags[:,:,i] = Ifs

# Ifs_means = Ifs_all_subtags.mean(axis=-1)

# np.save(f'/media/pat/datadrive/other-algo-crap/{tag}-If-means.npy', Ifs_means)






tag = 'agno3-d03'
print(tag)
It = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-targ.npy')

iter_counts = [i for i in range(121)]
Ifs_means = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-If-means.npy')



It = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-targ.npy')
iter_counts = [i for i in range(121)]
Ifs_means = np.load(f'/media/pat/datadrive/other-algo-crap/{tag}-If-means.npy')
iter_counts = [10,30,50,70, 90, 120]


c_vals = np.linspace(0, 1, len(iter_counts))
c_vals = [0, 0.2, 0.4, 0.65, 0.75, 0.85]
print(c_vals)
colors = cm.brg(c_vals)

# for i, (iter_count, color) in enumerate(zip(iter_counts, colors)):
    # fig, axes = plt.subplots(1,1,figsize=(5.28/2.54, 5.28/2.54), dpi=300 )
    # x =It/np.sum(It)*1000
    # y =Ifs_means[iter_count,:]/np.sum(Ifs_means[iter_count,:])*1000


#     print('\t\t', iter_count)
    # fit0 = np.polynomial.polynomial.Polynomial.fit(x, y, 1 )
    # print('fit0', fit0.convert().coef)

    # # fit1 = np.polynomial.polynomial.Polynomial.fit(x, y, 1, w = x  )
    # # print('fit1', fit1.convert().coef)

    # # fit2 = np.polynomial.polynomial.Polynomial.fit(x, y, 1, w = y  )
    # # print('fit2', fit2.convert().coef)
    # # print()

    # fit = np.polynomial.polynomial.Polynomial.fit(x, y, 1 )

    # # fit = np.polynomial.polynomial.Polynomial.fit(x, y, 1)

    # x_fit = np.linspace(0, 3, 50)
    # y_fit = fit(x_fit)
    # m = np.round(fit.convert().coef[1],2)
    # c = np.round(fit.convert().coef[0],2)


    # axes.plot(x,y, ls='', marker='.', color=color)
    
    # axes.plot([0,3], [0,3], ls='-.', marker='', color='k')
    # axes.text(0.1, 2.7, f'{iter_count} Iterations')

    # axes.set_ylim([0, 3])
    # axes.set_xlim([0, 3])
    # axes.set_ylabel('Norm. Recovered Intensity [AU]')
    # axes.set_xlabel('Norm. Target Intensity [AU]')

    # plt.tight_layout()


    # plt.savefig(f'/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_{tag}_inten_xy_{iter_count}.png')





apple = np.zeros(len(iter_counts))


rfs=['0.90', '0.77', '0.56', '0.23', '0.16', '0.18']
fig, axes = plt.subplots(2,3,figsize=(16/2.54, 8/2.54), dpi=300, sharex=True, sharey=True )
for i, (iter_count, color, ax, rf) in enumerate(zip(iter_counts, colors, axes.flatten(), rfs)):
    x =It/np.sum(It)*1000
    y =Ifs_means[iter_count,:]/np.sum(Ifs_means[iter_count,:])*1000


    apple[i] = np.sum(Ifs_means[iter_count,:])



    print('\t\t', iter_count)
    fit0 = np.polynomial.polynomial.Polynomial.fit(x, y, 1 )
    print('fit0', fit0.convert().coef)

    # fit1 = np.polynomial.polynomial.Polynomial.fit(x, y, 1, w = x  )
    # print('fit1', fit1.convert().coef)

    # fit2 = np.polynomial.polynomial.Polynomial.fit(x, y, 1, w = y  )
    # print('fit2', fit2.convert().coef)
    # print()

    fit = np.polynomial.polynomial.Polynomial.fit(x, y, 1 )

    # fit = np.polynomial.polynomial.Polynomial.fit(x, y, 1)

    x_fit = np.linspace(0, 3, 50)
    y_fit = fit(x_fit)
    m = np.round(fit.convert().coef[1],2)
    c = np.round(fit.convert().coef[0],2)


    ax.plot(x,y, ls='', marker='.', color=color, alpha=1,  mew=0, ms=5.0)
    
    ax.plot([0,3], [0,3], ls='-.', marker='', color='k')
    ax.text(0.1, 2.7, f'{iter_count} Iterations')
    ax.text(0.1, 2.3, f'$R$ factor: {rf}')

    ax.set_ylim([0, 3])
    ax.set_xlim([0, 3])

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.grid(False)

plt.ylabel('Norm. Recovered Intensity [AU]')
plt.xlabel('Norm. Target Intensity [AU]')
plt.subplots_adjust(
top=0.95,
bottom=0.15,
left=0.1,
right=0.95,
hspace=0.15,
wspace=0.1
)



plt.savefig(f'/home/pat/Documents/phd/figs/py/algo_{tag}_inten_xy_2x3.png')






# plt.figure()
# plt.plot(iter_counts, apple)








plt.show()



