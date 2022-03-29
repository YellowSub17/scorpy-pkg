#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')








tag = 'agno3-largerqmax'
sub_tags = ['testing']

# tag = 'p1-inten-r0-from-corr-qloose-supp'
# sub_tags = ['a', 'b', 'c']



# tag = 'anilinomethylphenol'
# sub_tags = ['a', 'b', 'c']


cmap = 'viridis'




for plotval in ['steps', 'rfactor', 'dist']:
# for plotval in ['steps']:
    plt.figure()
    for sub_tag, color in zip(sub_tags, 'rgb'):
        y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/{plotval}_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
        plt.plot(np.log10(y[1:]), label=f'{sub_tag}', color=color)
    plt.legend()
    plt.title(f'{tag} {plotval} (log)')

    plt.figure()
    for sub_tag, color in zip(sub_tags, 'rgb'):
        y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/{plotval}_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
        plt.plot(y[1:], label=f'{sub_tag}', color=color)
    plt.legend()
    plt.title(f'{tag} {plotval}')


plt.show()







ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
qloc = np.unique(np.where(st.vol !=0)[0])
print(qloc)

qq = 237
# qq = 140


ss.plot_slice(0, qq, title='supp', cmap=cmap)
fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
plt.tight_layout()
st.plot_slice(0, qq, title='targ', cmap=cmap, fig=fig, axes=axes.flatten()[0], log=False)
# st.plot_slice(0, qq, title='targ', cmap=cmap, log=False)
for i, sub_tag in enumerate(sub_tags):

    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    si = sf.copy()
    si.integrate_peaks(mask_vol=st , dpix=1)

    si.plot_slice(0,qq, title=f'{tag}_{sub_tag}', cmap=cmap, fig=fig, axes=axes.flatten()[i+1], log=False)

    rf = scorpy.utils.rfactor(si.vol/si.vol.sum(), st.vol/st.vol.sum())
    print(rf)


plt.figure()
plt.title('fsc')
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    si = sf.copy()
    si.integrate_peaks(mask_vol=st, dpix=1)
    fsc = scorpy.utils.fsc(si.vol, st.vol)
    plt.plot(fsc, label=f'{sub_tag}')
plt.legend()



plt.figure()
plt.title(f'fo vs fcalc (colored by theta)')
for i, sub_tag in enumerate(sub_tags):
    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    si = sf.copy()
    si.integrate_peaks(mask_vol=st, dpix=1)


    loc = np.where(st.vol>0)



    plt.scatter(st.vol[loc]/st.vol.sum(), si.vol[loc]/si.vol.sum(),c=loc[1], label=f'{sub_tag}', cmap='seismic')
    plt.title(f'Itarg vs Icalc (Coloured by Theta)')
    plt.xlabel('Itarg')
    plt.ylabel('Icalc')



plt.plot( [0, st.vol[loc].max()/st.vol.sum()],[0, st.vol[loc].max()/st.vol.sum()])
plt.colorbar()
plt.legend()















# st_flat = st.vol[st.vol>0].flatten()
# st_flat /= st_flat.sum()
# for i, sub_tag in enumerate(sub_tags):
    # sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
    # si = sf.copy()
    # si.integrate_peaks(mask_vol=st)

    # si_flat = si.vol[st.vol>0].flatten()
    # si_flat /= si_flat.sum()

    # plt.scatter(si_flat, st_flat, label=f'{sub_tag}')


# plt.plot( [0, st_flat.max()], [0, st_flat.max()])
# plt.legend()





















plt.show()
