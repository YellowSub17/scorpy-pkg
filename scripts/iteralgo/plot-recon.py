#!/usr/bin/env python3
import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')








tag = 'barite'
sub_tags = ['testing']



ciffname = 'barite'


# tag = 'p1-inten-r0-from-corr-qloose-supp'
# sub_tags = ['a', 'b', 'c']


# tag = 'anilinomethylphenol'
# sub_tags = ['a', 'b', 'c']




qq = 240




###load vols
ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
cif_t = scorpy.CifData(path=f'{scorpy.DATADIR}/algo/{tag}/{tag}_targ-sf.cif', rotk=[1,1,1], rottheta=np.radians(30), qmax=9)


qloc = np.unique(st.ls_pts(inds=1)[:,0])
print(qloc)
stepfig, stepaxes = plt.subplots(1,1)
rffig, rfaxes = plt.subplots(1,1)


for sub_tag in sub_tags:



    sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')

    si = sf.copy()
    si.integrate_peaks(mask_vol=st, dpix=2)


    cif_f = scorpy.CifData(path=f'{scorpy.DATADIR}/xtal/{ciffname}/{ciffname}.cif', rotk=[1,1,1], rottheta=np.radians(30))
    cif_f.fill_from_sphv(si, bragg_xyz=cif_t.scat_bragg[:,:3])


    R = cif_f.rfactor(cif_t)
    print('R factor:', R)




    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/steps_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    stepaxes.plot(np.log10(y[1:]), label=f'{sub_tag}')
    stepaxes.legend()
    stepaxes.set_xlabel('Iteration Number')
    stepaxes.set_ylabel('Iteration Step')

    y = np.loadtxt(f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/rfactor_{tag}_{sub_tag}.txt', delimiter=',', usecols=0)
    rfaxes.plot(y[1:], label=f'{sub_tag}')
    rfaxes.legend()
    rfaxes.set_xlabel('Iteration Number')
    rfaxes.set_ylabel('Rfactor')


    plt.figure()
    plt.title(f'{sub_tag} Rfactor: {np.round(R, 4)}')
    plt.scatter(cif_t.scat_bragg[:,-1]/cif_t.scat_bragg[:,-1].sum(),
                cif_f.scat_bragg[:,-1]/cif_f.scat_bragg[:,-1].sum(), c=cif_t.scat_sph[:,1], cmap='hsv')
    plt.xlabel('Itarg')
    plt.ylabel('Ialgo')
    plt.plot( [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum() ],
              [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum()])
    cb = plt.colorbar()
    cb.set_label('theta')


    plt.figure()
    plt.title(f'{sub_tag} Rfactor: {np.round(R, 4)}')
    plt.scatter(cif_t.scat_bragg[:,-1]/cif_t.scat_bragg[:,-1].sum(),
                cif_f.scat_bragg[:,-1]/cif_f.scat_bragg[:,-1].sum(), c=cif_t.scat_sph[:,0], cmap='hsv')
    plt.xlabel('Itarg')
    plt.ylabel('Ialgo')
    plt.plot( [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum() ],
              [0,cif_t.scat_bragg[:,-1].max()/cif_t.scat_bragg[:,-1].sum()])
    cb = plt.colorbar()
    cb.set_label('Q')





    st.plot_slice(0, qq, title='target')
    si.plot_slice(0, qq, title='integ')
    sf.plot_slice(0, qq, title='final')


    










plt.show()
