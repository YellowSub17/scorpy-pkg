#!/usr/bin/env python3

import scorpy
import numpy as np
import matplotlib.pyplot as plt
import time
import os
plt.close('all')





tag = 'x'

sample = 'nacl'
# self, ciffname, nq, nl, qmax, rotk, rottheta


nq = 256
nl = 180
qmax = 9
npsi = 360*32

lcrop=40
pinv_rcond=0.1

rotk = [1,1,1]

rottheta = np.radians(30)

dxsupp = 2


targ_cif_fname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}-sf.cif'
supp_cif_fname = f'{scorpy.DATADIR}/xtal/{sample}/{sample}.cif'

rec_fname =f'{scorpy.DATADIR}/algo/RECIPES/x.txt'


a = scorpy.AlgoHandler(tag=tag)





# # a.make_target(targ_cif_fname, nq, nl, qmax, rotk, rottheta, dxsupp, verbose=99)
# # a.make_support(supp_cif_fname, nq, nl, qmax, rotk, rottheta, dxsupp, verbose=99)



# # a.make_inputs(targ_cif_fname, supp_cif_fname, nq, npsi, nl, lcrop, qmax, rotk, rottheta, dxsupp, verbose=99)


# a.run_recon('x1', rec_fname, verbose=1)






