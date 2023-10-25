
import scorpy
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import numpy as np

plt.rc('font', size=8)



# nqs = list(range(25, 251, 25))
# nqs = [25,50, 75, 100, 150, 200, 250]
nqs = [ 50, 75,  100, 125, 150, 200]
# nls = list(range(60, 181, 15))

nls = [60, 90, 120, 135, 150, 180]


cmap_rf = cm.winter( np.linspace(0, 1, len(nqs)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nqs)))


#### nq




plt.rc('font', size=8)
fignqrf, axesnqrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )
fignqd, axesnqd = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )



loc = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-It-If-loc.npy')

iter_counts = [i for i in range(111)]


for i, nq in enumerate(nqs):
    print(f'{nq=}')
    if nq==150:
        a = scorpy.AlgoHandler(f'agno3-nl180')
    elif nq==200:
        a = scorpy.AlgoHandler(f'agno3-random-starts')
    else:
        a = scorpy.AlgoHandler(f'agno3-nq{nq}')
    # a.plot_vs_count('a', 'rfs', marker=',',linestyle='-',
                    # fig=fignqrf, axes=axesnqrf,  ylabel='Crystallographic $R$ Factor',color=cmap_rf[i],
                    # xerr=None, yerr=None, label=f'{nq}', xlabel='Algorithm Iteration')

    # # It = a.get_targ_inten()
    # # np.save(f'/media/pat/datadrive/other-algo-crap/{a.tag}-targ.npy', It)
    # # loc = a.get_It_If_loc('a')
    # # np.save(f'/media/pat/datadrive/other-algo-crap/{a.tag}-It-If-loc.npy',loc)



    It = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-targ.npy')
    loc = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-It-If-loc.npy')


    It = It/np.sum(It)
    If = a.get_inten_quick('a', iter_counts, loc)

    If = If/np.sum(If, axis=-1)[:,None]

    rfs = np.sum(np.abs(It - If), axis=-1) /np.sum( np.abs(If), axis=-1 )
    print(rfs.shape)

    axesnqrf.plot(iter_counts, rfs, marker=',', linestyle='-', color=cmap_rf[i], label=f'{nq}')
    # axesnqrf.plot(iter_counts, np.log10(rfs), marker=',', linestyle='-', color=cmap_rf[i], label=f'{nq}')
    axesnqrf.set_ylabel('Crystallographic $R$ Factor')
    axesnqrf.set_xlabel('Algorithm Iteration')


    # for iter_count in range(111):
        # print(f'{iter_count=}')

        # If = a.get_intensity('a', count=iter_count)




    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker=',', linestyle='-',
                    fig=fignqd, axes=axesnqd, color = cmap_atomic[i], ylabel='Mean Atomic Displacement [\u212B]',
                    xerr=None, yerr=None, label=f'{nq}', xlabel='Algorithm Iteration')


axesnqrf.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$n_q:$', ncol=2, frameon=False)
axesnqd.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$n_q:$', ncol=2, frameon=False)

axesnqrf.set_xlim(0, 110)
axesnqrf.set_ylim(0, 1.2)


axesnqd.set_xlim(0, 110)
axesnqd.set_ylim(0, 1.16)


fignqrf.tight_layout()
fignqd.tight_layout()

fignqrf.savefig('/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_samp_nqrf.png')
fignqd.savefig('/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_samp_nqd.png')







cmap_rf = cm.winter( np.linspace(0, 1, len(nls)))
cmap_atomic = cm.gist_heat( np.linspace(0, 0.75, len(nls)))



# #### nl

fignlrf, axesnlrf = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )
fignld, axesnld = plt.subplots(1,1,figsize=(8/2.54, 8/2.54), dpi=300, sharex=True )





for i, nl in enumerate(nls):
    print(f'{nl=}')
    a = scorpy.AlgoHandler(f'agno3-nl{nl}')

    # a.plot_vs_count('a', 'rfs', marker='',linestyle='-',
                    # fig=fignlrf, axes=axesnlrf, color = cmap_rf[i], ylabel='Crystallographic $R$ Factor',
                   # xerr=None, yerr=None, xlabel='Algorithm Iteration', label=f'{nl}')



    It = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-targ.npy')
    loc = np.load('/media/pat/datadrive/other-algo-crap/agno3-d07-It-If-loc.npy')


    It = It/np.sum(It)
    If = a.get_inten_quick('a', iter_counts, loc)

    If = If/np.sum(If, axis=-1)[:,None]

    rfs = np.sum(np.abs(It - If), axis=-1) /np.sum( np.abs(If), axis=-1 )
    print(rfs.shape)

    axesnlrf.plot(iter_counts, rfs, marker=',', linestyle='-', color=cmap_rf[i], label=f'{2*nl}')
    # axesnlrf.plot(iter_counts, np.log10(rfs), marker=',', linestyle='-', color=cmap_rf[i], label=f'{nl}')
    axesnlrf.set_ylabel('Crystallographic $R$ Factor')
    axesnlrf.set_xlabel('Algorithm Iteration')




    a.plot_vs_count('a', 'mean_dxyzs',logy=False, marker='',linestyle='-', label=f'{2*nl}',
                    fig=fignld, axes=axesnld, color = cmap_atomic[i], xerr=None, yerr=None,
                    ylabel='Mean Atomic Displacement [\u212B]', xlabel='Algorithm Iteration')

axesnlrf.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$n_\\theta:$', ncol=2, frameon=False)

axesnld.legend(bbox_to_anchor=(1,1), loc="upper right", framealpha=1, title='$n_\\theta:$', ncol=2, frameon=False)

axesnlrf.set_xlim(0, 110)
axesnlrf.set_ylim(0, 1.2)


axesnld.set_xlim(0, 110)
axesnld.set_ylim(0, 1.16)


fignlrf.tight_layout()
fignld.tight_layout()

fignlrf.savefig('/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_samp_nlrf.png')
fignld.savefig('/home/pat/Documents/phd/writing/iteralgopaper/figs/py/algo_samp_nld.png')
plt.show()


