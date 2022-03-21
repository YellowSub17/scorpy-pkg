


import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')





tag = 'nicotineamide-dres1-loose-supp-bigpsi-crop-poles'
sub_tag = 'b'


st = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
ss = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')
sf = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')



qloc = np.unique(np.where(ss.vol !=0)[0])
print(qloc)

qq = 78



fig, axes= plt.subplots(1,2)
st.plot_slice(0, qq, fig=fig, axes=axes[0])
sf.plot_slice(0, qq, fig=fig, axes=axes[1])






si = st.copy()

for pti in st.ls_pts(inds=True):


    xul = int(pti[0]-1), int(pti[0]+2)
    yul = int(pti[1]-1), int(pti[1]+2)
    zul = int(pti[2]-1), int(pti[2]+2)


    intenI = sf.vol[ xul[0]:xul[1], yul[0]:yul[1], zul[0]:zul[1] ].sum()

    si.vol[int(pti[0]), int(pti[1]), int(pti[2])] = intenI



fig, axes= plt.subplots(1,2)
st.plot_slice(0, qq, fig=fig, axes=axes[0], title='target')
si.plot_slice(0, qq, fig=fig, axes=axes[1], title='integrated')






plt.show()


