



import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')






qmax = 9
nq = 100
npsi = 360*32
nl = 180

rotk = [1,1,1]
rottheta = np.radians(30)


tag = 'copy-time-test'
sample = 'nacl'



targ_ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'
targ_insfname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}.ins'
supp_ciffname= f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif'




# a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta)
# a.make_target(targ_ciffname, targ_insfname, verbose=99)
# a.make_support(supp_ciffname, verbose=99)


# a.make_data(verbose=99)


a = scorpy.AlgoHandler(tag=tag)
sphv_init = scorpy.SphericalVol(a.nq, a.nl*2, a.nl*4, a.qmax)
sphv_init.vol = np.random.random(sphv_init.vol.shape)

print(sphv_init.vol[0,0,0])


a.run_recon('slow', f'{scorpy.DATADIR}/algo/RECIPES/rec_slow.txt', verbose=99, sphv_init=sphv_init)






















plt.show()

