



import scorpy
import numpy as np
np.random.seed(0)
import matplotlib.pyplot as plt
plt.close('all')





qmax = 9
nq = 150
npsi = 360*32

rotk = [1,1,1]
rottheta = np.radians(30)
sample = 'agno3'
ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'



for nl in [165, 135, 105, 75, 60]:
    tag = f'agno3-nl{nl}-x'


    a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta, overwrite=0)
    a.make_target(ciffname, verbose=99)
    a.make_support(ciffname,verbose=99, unit=True)



    a.make_data(verbose=99)

















plt.show()

