import scorpy
import numpy as np
import matplotlib.pyplot as plt



tag = 'p1_inten_r0_supp_t'
sub_tag = 'c'



sphv_targ = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_targ.dbin')
sphv_supp = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/sphv_{tag}_supp.dbin')

sphv_a = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_final.dbin')
sphv_a_init = scorpy.SphericalVol(path=f'{scorpy.DATADIR}/algo/{tag}/{sub_tag}/sphv_{tag}_{sub_tag}_init.dbin')

qq = np.unique(np.where(sphv_targ.vol>0)[0])




print('CSS of target vs initial (all positions)')
x = scorpy.utils.cosinesim(sphv_targ.vol, sphv_a_init.vol)
print(x)
print()

print('CSS of target vs initial (just peaks)')
x = scorpy.utils.cosinesim(sphv_targ.vol[sphv_supp.vol>0], sphv_a_init.vol[sphv_supp.vol>0])
print(x)
print()

print('CSS of target vs final (all positions)')
x = scorpy.utils.cosinesim(sphv_targ.vol, sphv_a.vol)
print(x)
print()

print('CSS of target vs final (just peaks)')
x = scorpy.utils.cosinesim(sphv_targ.vol[sphv_supp.vol>0], sphv_a.vol[sphv_supp.vol>0])
print(x)
print()

print('CSS of target vs initial (just peaks, scaled 0.75 to 1)')
x = scorpy.utils.cosinesim(sphv_targ.vol[sphv_supp.vol>0], sphv_a_init.vol[sphv_supp.vol>0])
print( (x-0.75)/(1-0.75))
print()

print('CSS of target vs final (just peaks, scaled 0.75 to 1)')
x = scorpy.utils.cosinesim(sphv_targ.vol[sphv_supp.vol>0], sphv_a.vol[sphv_supp.vol>0])
print( (x-0.75)/(1-0.75))
print()








plt.show()
