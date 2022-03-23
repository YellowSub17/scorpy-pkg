
import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')








tag = 'anilinomethylphenol'
sub_tag = 'long_er'



sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')


qloc = np.unique(np.where(sphv_targ.vol !=0)[0])
print(qloc)
qq = 120

sphv_noise = sphv_targ.copy()
# sphv_noise.vol *= 10
sphv_noise.vol += np.random.random(sphv_noise.vol.shape)*sphv_targ.vol*1
sphv_noise.vol *= sphv_supp.vol



# sphv_noise= scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
sphv_noise.integrate_peaks(mask_vol=sphv_targ)



sphv_targ.vol /= sphv_targ.vol.sum()
sphv_noise.vol /= sphv_noise.vol.sum()



fig, axes = plt.subplots(1,2, sharex=True, sharey=True)
sphv_targ.plot_slice(0, qq, fig=fig, axes=axes[0])
sphv_noise.plot_slice(0, qq, fig=fig, axes=axes[1])


rf = scorpy.utils.rfactor(sphv_noise.vol, sphv_targ.vol)
print(rf)


fsc = scorpy.utils.fsc(sphv_noise.vol, sphv_targ.vol)







plt.figure()
plt.plot(sphv_targ.qpts, fsc)







plt.show()




