



import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')





qmax = 9
npsi = 360*32

rotk = [1,1,1]
rottheta = np.radians(30)
sample = 'agno3'
ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'


nl = 180


nq = 150

# nqs = [ 25, 50, 75, 100, 125, 175, 225, 250]

# for nq in nqs:

tag = f'agno3-rec'
a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta, overwrite=0)
a.make_target(ciffname, verbose=99)
a.make_support(ciffname,verbose=99, unit=True)

a.make_data(verbose=99)

    # a.check_inputs(verbose=99)


















plt.show()

