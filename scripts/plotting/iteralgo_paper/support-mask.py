

import scorpy
import matplotlib.pyplot as plt
import numpy as np





# path=f'{scorpy.DATADIR}/algo/agno3-d03/sphv_agno3-d03_supp_loose.dbin'


# supp = scorpy.SphericalVol(path=path)




cif = scorpy.CifData(path='/media/pat/datadrive/xtal/agno3-d05/agno3-d05-sf.cif', rotk=[1,1,1], rottheta=10)

supp = scorpy.SphericalVol(20, 20, 40,cif.qmax)


supp.fill_from_cif(cif)

for i in range(1,4):



    fig, axes = plt.subplots(1,1,figsize=(2/2.54, 2/2.54), dpi=300, frameon=False )
    supp.plot_slice(0, i, xticks=[], yticks=[], cb=False, fig=fig, axes=axes)
    plt.tight_layout()
    fig.savefig(f'/home/pat/Documents/cloudstor/phd/writing/iteralgopaper/figs/py/target_q{i}.png')

plt.show()

