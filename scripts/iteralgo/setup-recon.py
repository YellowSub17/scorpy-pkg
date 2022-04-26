



import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')





qmax = 3
nq = 150
npsi = 360*32

rotk = [1,1,1]
rottheta = np.radians(30)
sample = 'agno3'
ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'



tag = 'x'
nl = 180

a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta, overwrite=0)
a.make_target(ciffname, verbose=99)
a.make_support(ciffname,verbose=99, unit=True)



a.make_data(verbose=99)


a.check_inputs(verbose=99)

a.run_recon('a', f'{scorpy.DATADIR}/algo/RECIPES/short_test.txt', verbose=99)

















plt.show()

