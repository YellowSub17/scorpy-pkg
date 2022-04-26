



import scorpy
import numpy as np
import sys



tag = 'agno3-random-starts'

sub_tags = ['a0', 'b0', 'c0', 'd0', 'e0']

for sub_tag in sub_tags:

    a = scorpy.AlgoHandler(tag)
    a.check_inputs()

    sphv_init = a.sphv_base.copy()
    sphv_init.vol = np.random.random(sphv_init.vol.shape)
    sphv_init.vol -= 0.5


    a.run_recon(sub_tag, f'{scorpy.DATADIR}/algo/RECIPES/HIOER110.txt', sphv_init=sphv_init, verbose=99)














