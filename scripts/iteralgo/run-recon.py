



import scorpy
import numpy as np
import matplotlib.pyplot as plt
plt.close('all')






qmax = 9
nq = 100
npsi = 360*32
nl = 180

rotk = [1,1,1]
rottheta = np.radians(30)


tag = 'triclinic'
sample = 'agno3'



targ_ciffname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'
targ_insfname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}.ins'
supp_ciffname= f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif'




# a = scorpy.AlgoHandler(tag=tag, nq=nq, qmax=qmax, npsi=npsi, nl=nl, rotk=rotk, rottheta=rottheta)
# a.make_target(targ_ciffname, targ_insfname, verbose=99)
# a.make_support(supp_ciffname, verbose=99)



# a.make_data(verbose=99)



a = scorpy.AlgoHandler(tag=tag)
a.run_recon('a', f'{scorpy.DATADIR}/algo/RECIPES/rec.txt', verbose=99)






















plt.show()

