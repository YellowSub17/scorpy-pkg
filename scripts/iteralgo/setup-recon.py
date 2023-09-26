



import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')





qmax = 9
npsi = 360*16

rotk = [1,1,1]
rottheta = np.radians(30)
sample = 'agno3'
ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'


nl = 250
nq = 300



tag = f'{sample}-d07'
a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta, overwrite=1)
a.make_target(ciffname, verbose=99)
a.make_support(ciffname,verbose=99)

# sphv_suppl =  scorpy.SphericalVol(path=f'{a.sphv_supp_loose_path()}')
# sphv_suppl_mask = sphv_suppl.copy()
# sphv_suppl_mask.make_mask()
# plt.figure()
# plt.plot(sphv_suppl.vol.sum(axis=-1).sum(axis=-1))

# sphv_suppl.plot_slice(0,295)



a.make_data(verbose=99)



















plt.show()

